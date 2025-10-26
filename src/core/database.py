from supabase import create_client, Client
from supabase.client import ClientOptions
from core.secrets import SUPABASE_URL, SUPABASE_KEY, SUPABASE_KEY_ADMIN
from typing import Annotated, Any
from fastapi import Depends
from core.middleware import AuthMiddleware

GetToken = Annotated[Any, Depends(AuthMiddleware.get_token)]

class Database:
    @staticmethod
    def get_db(token: GetToken) -> Client:
        URL = SUPABASE_URL
        KEY = SUPABASE_KEY # Publishable key

        if not URL or not KEY:
            raise ValueError("Missing Supabase credentials in environment variables")

        if not token:
            return create_client(URL, KEY)
        
        return create_client(URL, KEY,
            options=ClientOptions(
                headers= {"Authorization": f"Bearer {token}"}
            )
        )

    @staticmethod
    def get_db_admin() -> Client:
        URL = SUPABASE_URL
        KEY = SUPABASE_KEY_ADMIN

        if not URL or not KEY:
            raise ValueError("Missing Supabase credentials in environment variables")
        
        return create_client(URL, KEY)