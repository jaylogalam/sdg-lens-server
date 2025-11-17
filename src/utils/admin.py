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
            "email": user.email,
            "username": user.user_metadata.get('username'),
            "app_role": user.user_metadata.get('app_role'),
            "created_at": user.created_at.strftime(DATE_FORMAT),
            "last_sign_in_at": user.last_sign_in_at.strftime(DATE_FORMAT), # type: ignore
            "updated_at": user.updated_at.strftime(DATE_FORMAT) # type: ignore
        }

        return user_data