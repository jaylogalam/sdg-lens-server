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
            },
        }
    )
        
    @staticmethod
    def read_user(db: Client, id: str):
        user = db.auth.admin.get_user_by_id(id).user
        user_data = AdminUtils.format_user_data(user) # type: ignore

        return user_data

    @staticmethod
    def read_users(db: Client):
        users = db.auth.admin.list_users()
        response: list[dict[str, str]] = []
        for user in users:
            response.append(AdminUtils.format_user_data(user)) # type: ignore
            
        return response
    
    @staticmethod
    def update_user(db: Client, id: str, data: dict[str, str]):
        return db.auth.admin.update_user_by_id(id, data) # type: ignore

    @staticmethod
    def delete_user(db: Client, id: str):
        return db.auth.admin.delete_user(id)