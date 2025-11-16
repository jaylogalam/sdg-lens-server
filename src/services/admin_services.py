from supabase import Client

class AdminServices:
    @staticmethod
    def create_user(db: Client, email: str, password: str, user_metadata: dict[str, str]):
        return db.auth.admin.create_user(
        {
            "email": email,
            "password": password,
            "user_metadata": user_metadata,
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