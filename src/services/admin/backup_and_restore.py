# services/admin/backup_and_restore.py

from supabase import Client
from datetime import datetime, timezone, timedelta
from typing import Any
import json
from pathlib import Path

# Tables included in backup/restore
# Make sure your audit logs table is here (e.g. "logs")
TABLES = [
    "profiles",
    "history",
    "logs",
]

# Supabase Storage bucket name (create this bucket in Supabase)
BUCKET_NAME = "json-backups"


class Backup:
    PH_TZ = timezone(timedelta(hours=8))  # Philippine Time (UTC+8)

    # ---------- INTERNAL: label → slug ----------
    @staticmethod
    def _slugify_label(label: str) -> str:
        # keep only letters, numbers, dash, underscore
        safe = "".join(c if (c.isalnum() or c in "-_") else "-" for c in label)
        return safe.strip("-_")

    # ---------- CREATE BACKUP ----------
    @staticmethod
    def create(
        db: Client,
        folder: str | None = None,
        label: str | None = None,
    ) -> str:
        """
        Create a full JSON snapshot and upload it to Supabase Storage.

        Filename pattern (Philippine time):
          YYYY-MM-DDTHH-MM-SS[-slug]-backup.json

        Examples:
          2025-12-04T08-15-00-backup.json
          2025-12-04T08-20-00-before-migration-backup.json
        """

        snapshot: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tables": {},
            "auth_users": {},
        }

        # 1) Collect table data
        for table in TABLES:
            response = db.table(table).select("*").execute()
            data = getattr(response, "data", None)
            if data is None:
                raise RuntimeError(f"Error getting data from table '{table}'")
            snapshot["tables"][table] = data

        # 2) Collect auth users
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

        # 3) PH timestamp at front (sortable)
        now_ph = datetime.now(Backup.PH_TZ)
        ts = now_ph.strftime("%Y-%m-%dT%H-%M-%S")  # 19 chars

        # 4) Optional human label → slug
        slug = Backup._slugify_label(label) if label else ""
        if slug:
            base_name = f"{ts}-{slug}-backup.json"
        else:
            base_name = f"{ts}-backup.json"

        file_name = base_name
        if folder:
            folder = folder.strip("/")
            file_name = f"{folder}/{base_name}"

        # 5) Upload to Supabase Storage
        file_bytes = json.dumps(snapshot, default=str).encode("utf-8")
        storage = db.storage.from_(BUCKET_NAME)
        storage.upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": "application/json", "upsert": "false"},
        )

        return file_name

    # ---------- LIST BACKUPS ----------
    @staticmethod
    def list_backups(db: Client, folder: str | None = None) -> list[dict[str, Any]]:
        """
        List all JSON backup files, sorted (newest first),
        with timestamps converted to Philippine Time (UTC+8).
        """
        storage = db.storage.from_(BUCKET_NAME)

        if folder:
            prefix = folder.strip("/") + "/"
            files = storage.list(path=prefix)
        else:
            prefix = ""
            files = storage.list()

        if not files:
            return []

        json_files = [f for f in files if f.get("name", "").endswith(".json")]
        backups: list[dict[str, Any]] = []

        for f in json_files:
            name = f.get("name", "")
            if not name:
                continue

            file_name = prefix + name if prefix else name
            base = Path(name).name  # e.g. "2025-12-04T08-15-00-label-backup.json"

            # Timestamp is always first 19 chars: "YYYY-MM-DDTHH-MM-SS"
            ts_part = base[:19]

            try:
                # Interpret the timestamp as PH time
                dt_ph = datetime.strptime(ts_part, "%Y-%m-%dT%H-%M-%S").replace(
                    tzinfo=Backup.PH_TZ
                )
            except ValueError:
                continue

            label_human = dt_ph.strftime("%b %d, %Y, %I:%M %p PH Time")

            backups.append(
                {
                    "file_name": file_name,
                    "created_at": dt_ph.isoformat(),
                    "label": label_human,
                    "folder": folder,
                }
            )

        backups.sort(key=lambda b: b["created_at"], reverse=True)
        return backups

    # ---------- RAW BYTES FOR DOWNLOAD ----------
    @staticmethod
    def get_backup_bytes(db: Client, file_name: str) -> bytes:
        """
        Download the raw JSON backup file content from storage.
        Used by the download endpoint.
        """
        storage = db.storage.from_(BUCKET_NAME)
        file_bytes = storage.download(path=file_name)
        if not file_bytes:
            raise RuntimeError(f"Backup file '{file_name}' is empty or not found.")
        return file_bytes

    # ---------- INTERNAL: PICK LATEST FILE ----------
    @staticmethod
    def _get_latest_file(db: Client, folder: str | None = None) -> str:
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

        json_files = [f for f in files if f.get("name", "").endswith(".json")]
        if not json_files:
            raise RuntimeError(
                f"No JSON backup files (*.json) found in bucket '{BUCKET_NAME}'"
                + (f" under folder '{folder}'" if folder else "")
            )

        latest = sorted(json_files, key=lambda f: f["name"], reverse=True)[0]
        return prefix + latest["name"] if prefix else latest["name"]

    # ---------- RESTORE FROM STORAGE ----------
    @staticmethod
    def restore(
        db: Client,
        file_name: str | None = None,
        folder: str | None = None,
    ) -> str:
        """
        Restore from a backup JSON file stored in Supabase Storage.

        - If file_name is provided → restore that file.
        - If not → restore latest file (optionally within folder).
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

        return Backup._restore_from_bytes_common(db, file_bytes, file_name)

    # ---------- RESTORE FROM UPLOADED BYTES ----------
    @staticmethod
    def restore_from_bytes(db: Client, file_bytes: bytes) -> str:
        """
        Restore from a locally uploaded JSON backup file.

        Returns a label-like string (e.g. "uploaded-file" or created_at) for logs.
        """
        return Backup._restore_from_bytes_common(db, file_bytes, "<uploaded-file>")

    # ---------- INTERNAL SHARED RESTORE LOGIC ----------
    @staticmethod
    def _restore_from_bytes_common(
        db: Client,
        file_bytes: bytes,
        origin_name: str,
    ) -> str:
        if not file_bytes:
            raise RuntimeError(f"Backup file '{origin_name}' is empty.")

        try:
            snapshot = json.loads(file_bytes.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(
                f"Backup '{origin_name}' is not valid JSON: {e}"
            )

        tables = snapshot.get("tables", {})
        auth_snapshot = snapshot.get("auth_users", {})

        # ---------- AUTH USERS ----------
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

        # (a) Delete users that are NOT in snapshot_ids (created after backup)
        if snapshot_ids:
            for user in current_users:
                uid = str(user.id)
                if uid not in snapshot_ids:
                    db.auth.admin.delete_user(uid)

        # (b) Fetch final users AFTER deletion
        try:
            final_users = db.auth.admin.list_users()
        except Exception as e:
            raise RuntimeError(f"Failed to list auth users after cleanup: {e}")

        existing_auth_ids: set[str] = {str(u.id) for u in final_users}

        # (c) Reset email + metadata for existing users
        for user in final_users:
            uid = str(user.id)
            if uid in snapshot_by_id:
                snap_user = snapshot_by_id[uid]
                email = snap_user.get("email")
                user_metadata = snap_user.get("user_metadata") or {}

                update_data: dict[str, Any] = {"user_metadata": user_metadata}
                if email:
                    update_data["email"] = email

                db.auth.admin.update_user_by_id(uid, update_data)

        # ---------- TABLES: wipe & re-insert ----------
        for table_name, rows in tables.items():
            # Delete all rows (using created_at to satisfy filter requirement).
            # Assumes these tables have a created_at column.
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

        return origin_name


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