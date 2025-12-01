from supabase import Client
from datetime import datetime, timezone, timedelta
from typing import Any
import json
from pathlib import Path

# Tables included in backup/restore
TABLES = [
    "profiles",
    "history",
    "logs",
]

# Supabase Storage bucket name
BUCKET_NAME = "json-backups"


class Backup:
    # Philippines Time (UTC+8)
    PH_TZ = timezone(timedelta(hours=8))

    # -------------------- CREATE BACKUP --------------------
    @staticmethod
    def create(db: Client, folder: str | None = None) -> str:

        snapshot: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tables": {},
            "auth_users": {},
        }

        # 1) Dump each app table
        for table in TABLES:
            response = db.table(table).select("*").execute()
            data = getattr(response, "data", None)
            if data is None:
                raise RuntimeError(f"Error getting data from table '{table}'")
            snapshot["tables"][table] = data

        # 2) Dump auth users
        try:
            users = db.auth.admin.list_users()
            users_data = []
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

        # 3) Filename (UTC-based)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
        file_name = f"{ts}-backup.json"

        if folder:
            folder = folder.strip("/")
            file_name = f"{folder}/{file_name}"

        # 4) Serialize to bytes
        file_bytes = json.dumps(snapshot, default=str).encode("utf-8")

        # 5) Upload to Supabase Storage
        storage = db.storage.from_(BUCKET_NAME)
        storage.upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": "application/json", "upsert": "false"},
        )

        return file_name

    # -------------------- LIST BACKUPS --------------------
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

        backups = []

        for f in json_files:
            name = f.get("name", "")
            if not name:
                continue

            file_name = prefix + name if prefix else name
            base = Path(name).name
            ts_str = base.replace("-backup.json", "")

            try:
                # parse as UTC
                dt_utc = datetime.strptime(ts_str, "%Y-%m-%dT%H-%M-%S").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                continue

            # Convert to PH time
            dt_ph = dt_utc.astimezone(Backup.PH_TZ)

            # Pretty label
            label = dt_ph.strftime("%b %d, %Y, %I:%M %p PH Time")

            backups.append(
                {
                    "file_name": file_name,
                    "created_at": dt_ph.isoformat(),
                    "label": label,
                    "folder": folder,
                }
            )

        # Sort newest → oldest (by PH time)
        backups.sort(key=lambda b: b["created_at"], reverse=True)

        return backups

    # -------------------- RAW BYTES FOR DOWNLOAD --------------------
    @staticmethod
    def get_backup_bytes(db: Client, file_name: str) -> bytes:
        storage = db.storage.from_(BUCKET_NAME)
        file_bytes = storage.download(path=file_name)
        if not file_bytes:
            raise RuntimeError(f"Backup file '{file_name}' is empty or not found.")
        return file_bytes

    # -------------------- INTERNAL: GET LATEST --------------------
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
            raise RuntimeError("No JSON backups found.")

        latest = sorted(json_files, key=lambda f: f["name"], reverse=True)[0]

        return prefix + latest["name"] if prefix else latest["name"]

    # -------------------- RESTORE --------------------
    @staticmethod
    def restore(db: Client, file_name: str | None = None, folder: str | None = None):
        storage = db.storage.from_(BUCKET_NAME)

        if not file_name:
            file_name = Backup._get_latest_file(db, folder)

        file_bytes = storage.download(path=file_name)
        if not file_bytes:
            raise RuntimeError("Backup file is empty.")

        snapshot = json.loads(file_bytes.decode("utf-8"))

        tables = snapshot.get("tables", {})
        snapshot_users = snapshot.get("auth_users", {}).get("users") or []

        # ================= AUTH RESTORE =================

        snapshot_by_id = {str(u["id"]): u for u in snapshot_users}
        snapshot_ids = set(snapshot_by_id.keys())

        current_users = db.auth.admin.list_users()

        # Delete new users NOT in backup
        for user in current_users:
            uid = str(user.id)
            if uid not in snapshot_ids:
                db.auth.admin.delete_user(uid)

        # Get final users (after deletion)
        final_users = db.auth.admin.list_users()
        existing_ids = {str(u.id) for u in final_users}

        # Reset metadata + email
        for user in final_users:
            uid = str(user.id)
            if uid in snapshot_by_id:
                snap = snapshot_by_id[uid]
                db.auth.admin.update_user_by_id(
                    uid,
                    {
                        "email": snap.get("email"),
                        "user_metadata": snap.get("user_metadata") or {},
                    },
                )

        # ================= TABLE RESTORE =================

        for table, rows in tables.items():
            # clear table
            db.table(table).delete().gte("created_at", "1900-01-01T00:00:00Z").execute()

            if not rows:
                continue

            good_rows = []
            for row in rows:
                if "user_id" in row:
                    if str(row["user_id"]) in existing_ids:
                        good_rows.append(row)
                else:
                    good_rows.append(row)

            if good_rows:
                db.table(table).insert(good_rows).execute()

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