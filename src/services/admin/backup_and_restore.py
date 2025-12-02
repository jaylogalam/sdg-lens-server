# services/admin/backup_and_restore.py

from supabase import Client
from datetime import datetime, timezone, timedelta
from typing import Any
import json
from pathlib import Path

TABLES = [
    "profiles",
    "history",
    "logs",
]

BUCKET_NAME = "json-backups"


class Backup:
    PH_TZ = timezone(timedelta(hours=8))

    # ---------- CREATE BACKUP ----------
    @staticmethod
    def create(db: Client, folder: str | None = None) -> str:
        snapshot: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tables": {},
            "auth_users": {},
        }

        # 1) application tables
        for table in TABLES:
            response = db.table(table).select("*").execute()
            data = getattr(response, "data", None)
            if data is None:
                raise RuntimeError(f"Error getting data from table '{table}'")
            snapshot["tables"][table] = data

        # 2) auth users
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

        # 3) filename (UTC, lexicographically sortable)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
        file_name = f"{ts}-backup.json"

        if folder:
            folder = folder.strip("/")
            file_name = f"{folder}/{file_name}"

        file_bytes = json.dumps(snapshot, default=str).encode("utf-8")

        storage = db.storage.from_(BUCKET_NAME)
        storage.upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": "application/json", "upsert": "false"},
        )

        return file_name

    # ---------- LIST BACKUPS (for dropdown) ----------
    @staticmethod
    def list_backups(db: Client, folder: str | None = None) -> list[dict[str, Any]]:
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
            base = Path(name).name
            ts_str = base.replace("-backup.json", "")

            try:
                dt_utc = datetime.strptime(ts_str, "%Y-%m-%dT%H-%M-%S").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                continue

            dt_ph = dt_utc.astimezone(Backup.PH_TZ)
            label = dt_ph.strftime("%b %d, %Y, %I:%M %p PH Time")

            backups.append(
                {
                    "file_name": file_name,
                    "created_at": dt_ph.isoformat(),
                    "label": label,
                    "folder": folder,
                }
            )

        backups.sort(key=lambda b: b["created_at"], reverse=True)
        return backups

    # ---------- DOWNLOAD BYTES (for download endpoint) ----------
    @staticmethod
    def get_backup_bytes(db: Client, file_name: str) -> bytes:
        storage = db.storage.from_(BUCKET_NAME)
        file_bytes = storage.download(path=file_name)
        if not file_bytes:
            raise RuntimeError(f"Backup file '{file_name}' is empty or not found.")
        return file_bytes

    # ---------- INTERNAL: pick latest ----------
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
            raise RuntimeError("No backup files available.")

        json_files = [f for f in files if f.get("name", "").endswith(".json")]
        if not json_files:
            raise RuntimeError("No JSON backup files found.")

        latest = sorted(json_files, key=lambda f: f["name"], reverse=True)[0]
        return prefix + latest["name"] if prefix else latest["name"]

    # ---------- INTERNAL: apply snapshot (time-travel logic here) ----------
    @staticmethod
    def _apply_snapshot(db: Client, snapshot: dict[str, Any]) -> None:
        """
        Apply a snapshot to the database.

        Rules:
        - DO NOT delete auth users (auth.users rows are never destroyed).
        - Users not present in snapshot → soft disabled via user_metadata.disabled = True.
        - Users present in snapshot → email + user_metadata overwritten from snapshot.
        - App tables (profiles, history, logs) are fully replaced by snapshot content.
        """

        tables = snapshot.get("tables", {})
        auth_snapshot = snapshot.get("auth_users", {})

        # 1) snapshot users map
        snapshot_users = auth_snapshot.get("users") or []
        snapshot_by_id: dict[str, dict[str, Any]] = {}
        for u in snapshot_users:
            uid = str(u.get("id", ""))
            if uid:
                snapshot_by_id[uid] = u

        snapshot_ids: set[str] = set(snapshot_by_id.keys())

        # 2) current auth users (we never delete these)
        try:
            current_users = db.auth.admin.list_users()
        except Exception as e:
            raise RuntimeError(f"Failed to list current auth users: {e}")

        # 3) update/soft-disable users
        for user in current_users:
            uid = str(user.id)
            current_meta = getattr(user, "user_metadata", {}) or {}

            if uid in snapshot_ids:
                # user exists in snapshot → restore from snapshot
                snap_user = snapshot_by_id[uid]
                email = snap_user.get("email")
                user_metadata = snap_user.get("user_metadata") or {}

                update_data: dict[str, Any] = {
                    "user_metadata": user_metadata,
                }
                if email:
                    update_data["email"] = email

                db.auth.admin.update_user_by_id(uid, update_data)
            else:
                # not in snapshot → soft disable
                new_meta = dict(current_meta)
                new_meta["disabled"] = True
                new_meta["disabled_by_restore"] = True
                db.auth.admin.update_user_by_id(uid, {"user_metadata": new_meta})

        # 4) replace table data exactly with snapshot
        for table_name, rows in tables.items():
            # wipe table (using generic filter)
            db.table(table_name).delete().gte(
                "created_at", "1900-01-01T00:00:00Z"
            ).execute()

            if not rows:
                continue

            if isinstance(rows, list):
                to_insert = rows
            else:
                to_insert = rows

            db.table(table_name).insert(to_insert).execute()

    # ---------- RESTORE FROM STORAGE ----------
    @staticmethod
    def restore(db: Client, file_name: str | None = None, folder: str | None = None) -> str:
        storage = db.storage.from_(BUCKET_NAME)

        if not file_name:
            file_name = Backup._get_latest_file(db, folder)

        file_name = str(file_name)
        file_bytes = storage.download(path=file_name)
        if not file_bytes:
            raise RuntimeError(f"Backup file '{file_name}' is empty.")

        try:
            snapshot = json.loads(file_bytes.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Backup file '{file_name}' is not valid JSON: {e}")

        Backup._apply_snapshot(db, snapshot)
        return file_name

    # ---------- RESTORE FROM UPLOADED FILE ----------
    @staticmethod
    def restore_from_bytes(db: Client, file_bytes: bytes) -> str:
        if not file_bytes:
            raise RuntimeError("Uploaded backup file is empty.")

        try:
            snapshot = json.loads(file_bytes.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Uploaded backup is not valid JSON: {e}")

        Backup._apply_snapshot(db, snapshot)
        return "uploaded-backup.json"

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