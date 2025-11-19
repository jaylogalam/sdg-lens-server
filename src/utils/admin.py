from pydantic import BaseModel
from datetime import datetime
from typing import Any

class UserData(BaseModel):
    id: str
    email: str
    user_metadata: dict[str, Any]
    created_at: datetime
    last_sign_in_at: datetime
    updated_at: datetime

class AdminUtils:
    @staticmethod
    def format_user_data(user: UserData):
        DATE_FORMAT = "%c"
        user_data: dict[str, str] = {
            "user_id": user.id,
            "email": user.email if user.email else "",
            "username": user.user_metadata.get('username') if user.user_metadata.get('username') else "",
            "app_role": user.user_metadata.get('app_role') if user.user_metadata.get('app_role') else "",
            "created_at": user.created_at.strftime(DATE_FORMAT) if user.created_at else "",
            "last_sign_in_at": user.last_sign_in_at.strftime(DATE_FORMAT) if user.last_sign_in_at else "", # type: ignore
            "updated_at": user.updated_at.strftime(DATE_FORMAT) if user.updated_at else "" # type: ignore
        }

        return user_data