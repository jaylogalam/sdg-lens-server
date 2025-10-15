from supabase import create_client, Client

SUPABASE_URL = "https://duxqgefxnyrnlymsauso.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1eHFnZWZ4bnlybmx5bXNhdXNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5NDAxMzAsImV4cCI6MjA3NDUxNjEzMH0.KpKohNP5fOlcGeC2s2rdArCmsTcZHb9CaX7ez-3Eh0A"

class SupabaseClient:
    _instance: Client | None = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance

class DatabaseServices:    
    client: Client = SupabaseClient.get_client()
    
    @classmethod
    def read_item(cls, table: str):
        response = cls.client.table(table).select("*").execute()
        return response

    @classmethod
    def create_item(cls, table: str, data) -> None:
        response = cls.client.table(table).insert(data).execute()

    # def update_item(table: str, id: str, column: str) -> None:
    #     ...

    # def delete_item(table: str, id: str) -> None:
    #     response = client.table(table).delete().eq("id", id).execute()