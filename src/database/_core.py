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