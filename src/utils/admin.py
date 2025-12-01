# utils/admin.py
from pydantic import BaseModel
from datetime import datetime
from typing import Any


class UserData(BaseModel):
    id: str
    email: str | None = None
    user_metadata: dict[str, Any]
    created_at: datetime | None = None
    last_sign_in_at: datetime | None = None
    updated_at: datetime | None = None


class AdminUtils:
    @staticmethod
    def format_user_data(user: Any):
        """
        Normalizes Supabase auth user into a flat dict for the frontend.
        Includes 'disabled' flag from user_metadata.
        """
        DATE_FORMAT = "%c"

        # Supabase user object may not be a Pydantic model; we just access attrs safely
        user_metadata = getattr(user, "user_metadata", {}) or {}

        username = user_metadata.get("username") or ""
        app_role = user_metadata.get("app_role") or ""
        disabled = bool(user_metadata.get("disabled", False))

        created_at = getattr(user, "created_at", None)
        last_sign_in_at = getattr(user, "last_sign_in_at", None)
        updated_at = getattr(user, "updated_at", None)

        user_data: dict[str, Any] = {
            "user_id": str(getattr(user, "id", "")),
            "email": getattr(user, "email", "") or "",
            "username": username,
            "app_role": app_role,
            "disabled": disabled,
            "created_at": created_at.strftime(DATE_FORMAT) if created_at else "",
            "last_sign_in_at": last_sign_in_at.strftime(DATE_FORMAT) if last_sign_in_at else "",
            "updated_at": updated_at.strftime(DATE_FORMAT) if updated_at else "",
        }

        return user_data
