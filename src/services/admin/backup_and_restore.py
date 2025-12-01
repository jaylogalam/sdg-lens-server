# services/admin/backup_and_restore.py

from supabase import Client
from datetime import datetime, timezone
from typing import Any
import json

# Tables included in backup/restore
TABLES = [
    "profiles",
    "history",
    "logs",
]

# Supabase Storage bucket name
BUCKET_NAME = "json-backups"


class Backup:
    @staticmethod
    def create(db: Client, folder: str | None = None) -> str:
        """
        Create a full JSON snapshot of:
        - selected database tables (TABLES)
        - current auth users (id, email, user_metadata, timestamps)

        and upload it as a JSON file to Supabase Storage.
        """
        snapshot: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tables": {},
            "auth_users": {},
        }

        # --- 1) Collect data for each application table ---
        for table in TABLES:
            response = db.table(table).select("*").execute()
            data = getattr(response, "data", None)

            if data is None:
                raise RuntimeError(f"Error getting data from table '{table}'")

            snapshot["tables"][table] = data

        # --- 2) Collect current auth users (full info so we can restore disabled flag etc.) ---
        try:
            users = db.auth.admin.list_users()
            users_data: list[dict[str, Any]] = []

            for user in users:
                users_data.append(
                    {
                        "id": str(user.id),
                        "email": getattr(user, "email", None),
                        "user_metadata": getattr(user, "user_metadata", {}) or {},
                        "created_at": getattr(user, "created_at", None),
                        "last_sign_in_at": getattr(user, "last_sign_in_at", None),
                        "updated_at": getattr(user, "updated_at", None),
                    }
                )

            snapshot["auth_users"]["users"] = users_data
        except Exception as e:
            snapshot["auth_users"]["error"] = f"Failed to list auth users: {e}"

        # --- 3) Build filename ---
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
        file_name = f"{ts}-backup.json"

        if folder:
            folder = folder.strip("/")
            file_name = f"{folder}/{file_name}"

        # --- 4) Serialize snapshot to bytes ---
        file_bytes = json.dumps(snapshot, default=str).encode("utf-8")

        # --- 5) Upload to Supabase Storage ---
        storage = db.storage.from_(BUCKET_NAME)
        storage.upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": "application/json", "upsert": "false"},
        )

        return file_name

    @staticmethod
    def _get_latest_file(db: Client, folder: str | None = None) -> str:
        """
        Return the path of the latest JSON backup file in the bucket.

        - Only considers files ending with ".json".
        - If folder is provided: looks only inside that folder.
        - If no files exist: raises RuntimeError.
        """
        storage = db.storage.from_(BUCKET_NAME)

        if folder:
            prefix = folder.strip("/") + "/"
            files = storage.list(path=prefix)
        else:
            prefix = ""
            files = storage.list()

        if not files:
            raise RuntimeError(
                f"No files found in bucket '{BUCKET_NAME}'"
                + (f" under folder '{folder}'" if folder else "")
            )

        # Only keep .json files
        json_files = [f for f in files if f.get("name", "").endswith(".json")]

        if not json_files:
            raise RuntimeError(
                f"No JSON backup files (*.json) found in bucket '{BUCKET_NAME}'"
                + (f" under folder '{folder}'" if folder else "")
            )

        latest = sorted(json_files, key=lambda f: f["name"], reverse=True)[0]

        if prefix:
            return prefix + latest["name"]
        return latest["name"]

    @staticmethod
    def restore(
        db: Client,
        file_name: str | None = None,
        folder: str | None = None,
    ) -> str:
        """
        Restore from a backup JSON file.

        - If file_name is provided → restore that file.
        - If not → restore latest file (optionally within folder).

        Behavior:
        - Restores selected DB tables (TABLES)
        - Auth users:
            * deletes users created after backup
            * DOES NOT recreate deleted users
            * resets email + user_metadata (including `disabled`) for users that still exist
        - Any table rows whose user_id no longer exists in auth.users are skipped
          to avoid foreign key violations.
        """
        storage = db.storage.from_(BUCKET_NAME)

        # 1) Decide which file to use
        if not file_name:
            file_name = Backup._get_latest_file(db, folder)

        file_name = str(file_name)

        # 2) Download snapshot
        try:
            file_bytes = storage.download(path=file_name)
        except Exception as e:
            raise RuntimeError(f"Failed to download backup file '{file_name}': {e}")

        if not file_bytes:
            raise RuntimeError(f"Backup file '{file_name}' is empty.")

        try:
            snapshot = json.loads(file_bytes.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(
                f"Backup file '{file_name}' is not valid JSON: {e}"
            )

        tables = snapshot.get("tables", {})
        auth_snapshot = snapshot.get("auth_users", {})

        # ---------- 3) AUTH USERS: delete new ones, reset metadata on existing ----------

        snapshot_users = auth_snapshot.get("users") or []
        snapshot_by_id: dict[str, dict[str, Any]] = {}
        for u in snapshot_users:
            uid = str(u.get("id", ""))
            if uid:
                snapshot_by_id[uid] = u

        snapshot_ids: set[str] = set(snapshot_by_id.keys())

        # Current users BEFORE cleanup
        try:
            current_users = db.auth.admin.list_users()
        except Exception as e:
            raise RuntimeError(f"Failed to list current auth users: {e}")

        current_ids = {str(u.id) for u in current_users}

        # (a) Delete users that are NOT in snapshot_ids (created after backup)
        for user in current_users:
            uid = str(user.id)
            if snapshot_ids and uid not in snapshot_ids:
                db.auth.admin.delete_user(uid)

        # (b) Fetch final users AFTER deletion
        try:
            final_users = db.auth.admin.list_users()
        except Exception as e:
            raise RuntimeError(f"Failed to list auth users after cleanup: {e}")

        existing_auth_ids: set[str] = {str(u.id) for u in final_users}

        # (c) Reset email + metadata (including disabled) for users that still exist
        for user in final_users:
            uid = str(user.id)
            if uid in snapshot_by_id:
                snap_user = snapshot_by_id[uid]
                email = snap_user.get("email")
                user_metadata = snap_user.get("user_metadata") or {}

                update_data: dict[str, Any] = {
                    "user_metadata": user_metadata,
                }
                if email:
                    update_data["email"] = email

                db.auth.admin.update_user_by_id(uid, update_data)

        # ---------- 4) TABLES: delete all rows, then insert only rows whose user_id still exists ----------

        for table_name, rows in tables.items():
            # Delete all rows from this table
            db.table(table_name).delete().gte(
                "created_at", "1900-01-01T00:00:00Z"
            ).execute()

            if not rows:
                continue

            filtered_rows = []

            if isinstance(rows, list):
                for row in rows:
                    if isinstance(row, dict) and "user_id" in row:
                        uid = str(row.get("user_id"))
                        if uid in existing_auth_ids:
                            filtered_rows.append(row)
                    else:
                        # Table without user_id → keep as-is
                        filtered_rows.append(row)
            else:
                filtered_rows = rows

            if filtered_rows:
                db.table(table_name).insert(filtered_rows).execute()

        return file_name







# OLD CODE USING CSV BACKUPS

# from supabase import Client
# import pandas as pd
# from datetime import datetime
# from pathlib import Path

# tables = [
#     {"schema": "public", "table": "profiles"},
#     {"schema": "public", "table": "history"},
#     {"schema": "public", "table": "logs"},
# ]

# class Backup:
#     @staticmethod
#     def create(db: Client):
#         for table in tables:
#             response = db.table(table["table"]).select("*").execute()
            
#             if not response:
#                 raise RuntimeError(f"Error getting data from {table["schema"]}.{table['table']}")

#             df = pd.DataFrame(response.data)

#             date = datetime.now()
#             date = str(date.strftime("%Y;%m;%d-%H;%M;%S"))
#             save_path = Path(f'{date}-{table["schema"].upper()}{table['table']}.csv')
#             save_path.parent.mkdir(parents=True, exist_ok=True)
#             df.to_csv(save_path, index=False)