from supabase import Client
from pydantic import BaseModel

class NewUserTypes(BaseModel):
    email: str
    password: str
    user_metadata: dict[str, str]

class AdminServices:
    @staticmethod
    def create_user(db: Client, data: NewUserTypes):
        return db.auth.admin.create_user(
        {
            "email": data.email,
            "password": data.password,
            "user_metadata": data.user_metadata,
        }
    )
        
    @staticmethod
    def read_user(db: Client, id: str | None = None):
        if not id:
            return db.auth.admin.list_users()

        return db.auth.admin.get_user_by_id(id)

    @staticmethod
    def update_user(db: Client, id: str, data: dict[str, str]):
        return db.auth.admin.update_user_by_id(id, data) # type: ignore

    @staticmethod
    def delete_user(db: Client, id: str):
        return db.auth.admin.delete_user(id)