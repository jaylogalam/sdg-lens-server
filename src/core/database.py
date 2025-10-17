from supabase import create_client, Client
from core import Secrets

class Database:
    @staticmethod
    def get_db() -> Client:
        SUPABASE_URL = Secrets.SUPABASE_URL
        SUPABASE_KEY = Secrets.SUPABASE_KEY

        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Missing Supabase credentials in environment variables")
        
        return create_client(SUPABASE_URL, SUPABASE_KEY)
