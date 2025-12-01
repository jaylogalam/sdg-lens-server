# services/admin_services.py
from supabase import Client
from utils.admin import AdminUtils


class AdminServices:
    @staticmethod
    def create_user(db: Client, email: str, password: str, username: str):
        return db.auth.admin.create_user(
            {
                "email": email,
                "password": password,
                "user_metadata": {
                    "username": username,
                    "app_role": "user",
                    "disabled": False,  # 👈 new field
                },
            }
        )

    @staticmethod
    def read_user(db: Client, id: str):
        user = db.auth.admin.get_user_by_id(id).user
        user_data = AdminUtils.format_user_data(user)  # type: ignore
        return user_data

    @staticmethod
    def read_users(db: Client):
        """
        Return NON-admin users that are not disabled.
        """
        users = db.auth.admin.list_users()
        response: list[dict[str, str]] = []

        for user in users:
            user_data = AdminUtils.format_user_data(user)  # type: ignore

            app_role = user_data.get("app_role")
            disabled = user_data.get("disabled", False)

            # Only normal users, skip admins and disabled
            if app_role == "user" and not disabled:
                response.append(user_data)

        return response

    @staticmethod
    def read_admins(db: Client):
        """
        Return admin users that are not disabled.
        """
        users = db.auth.admin.list_users()
        response: list[dict[str, str]] = []

        for user in users:
            user_data = AdminUtils.format_user_data(user)  # type: ignore

            app_role = user_data.get("app_role")
            disabled = user_data.get("disabled", False)

            if app_role == "admin" and not disabled:
                response.append(user_data)

        return response

    @staticmethod
    def update_user(db: Client, id: str, username: str, app_role: str):
        """
        Update username + app_role.
        Keeps existing `disabled` flag as-is.
        """
        # Fetch current user to preserve disabled flag
        current = db.auth.admin.get_user_by_id(id).user
        current_metadata = getattr(current, "user_metadata", {}) or {}
        disabled = current_metadata.get("disabled", False)

        return db.auth.admin.update_user_by_id(
            id,
            {
                "user_metadata": {
                    "username": username,
                    "app_role": app_role,
                    "disabled": disabled,
                }
            },
        )

    @staticmethod
    def delete_user(db: Client, id: str):
        """
        SOFT DELETE:
        - Mark user as disabled = True (so hidden in UI)
        - Keep them in auth.users so restore can bring them back.
        """
        # You could also clear app_role or username if you want, but usually not needed.
        current = db.auth.admin.get_user_by_id(id).user
        current_metadata = getattr(current, "user_metadata", {}) or {}

        username = current_metadata.get("username", "")
        app_role = current_metadata.get("app_role", "user")

        return db.auth.admin.update_user_by_id(
            id,
            {
                "user_metadata": {
                    "username": username,
                    "app_role": app_role,
                    "disabled": True,  # 👈 this flags them as "deleted"
                }
            },
        )
