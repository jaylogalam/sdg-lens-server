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
        - current auth user IDs

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

        # --- 2) Collect current auth user IDs (for cleanup on restore) ---
        try:
            users = db.auth.admin.list_users()
            user_ids: list[str] = []
            for user in users:
                user_ids.append(str(user.id))

            snapshot["auth_users"]["user_ids"] = user_ids
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
        Return the path of the latest backup JSON file in the bucket.

        - If folder is provided: looks only inside that folder.
        - If no files exist: raises RuntimeError.
        """
        storage = db.storage.from_(BUCKET_NAME)

        if folder:
            prefix = folder.strip("/") + "/"
            files = storage.list(path=prefix)
        else:
            prefix = ""
            files = storage.list()  # list from bucket root

        if not files:
            raise RuntimeError(
                f"No backup files found in bucket '{BUCKET_NAME}'"
                + (f" under folder '{folder}'" if folder else "")
            )

        # Files are dicts like {"name": "2025-11-29T10-30-00-backup.json", ...}
        latest = sorted(files, key=lambda f: f["name"], reverse=True)[0]

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

        This restores:
        - selected DB tables (TABLES)
        - auth users: removes any user created after the backup
        """
        storage = db.storage.from_(BUCKET_NAME)

        # 1) Decide which file to use
        if not file_name:
            file_name = Backup._get_latest_file(db, folder)

        file_name = str(file_name)

        # 2) Download snapshot
        file_bytes = storage.download(path=file_name)
        snapshot = json.loads(file_bytes.decode("utf-8"))

        tables = snapshot.get("tables", {})
        auth_snapshot = snapshot.get("auth_users", {})

        # --- 3) Restore application tables ---
        for table_name, rows in tables.items():
            # Delete all rows using created_at as a "delete all" filter
            db.table(table_name).delete().gte(
                "created_at", "1900-01-01T00:00:00Z"
            ).execute()

            if rows:
                db.table(table_name).insert(rows).execute()

        # --- 4) Cleanup auth users: remove those created after backup ---
        user_ids = auth_snapshot.get("user_ids")
        if isinstance(user_ids, list):
            allowed_ids = {str(uid) for uid in user_ids}

            try:
                current_users = db.auth.admin.list_users()
                for user in current_users:
                    uid = str(user.id)
                    if uid not in allowed_ids:
                        # This user did not exist at backup time -> delete
                        db.auth.admin.delete_user(uid)
            except Exception as e:
                raise RuntimeError(f"Error restoring auth users: {e}")

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