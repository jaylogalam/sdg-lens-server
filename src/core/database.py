from supabase import create_client, Client
from core.secrets import SUPABASE_URL, SUPABASE_KEY

class Database:
    @staticmethod
    def get_db() -> Client:
        URL = SUPABASE_URL
        KEY = SUPABASE_KEY

        if not URL or not KEY:
            raise ValueError("Missing Supabase credentials in environment variables")
        
        return create_client(URL, KEY)
