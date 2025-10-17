from fastapi import Request
from supabase import create_client, Client

SUPABASE_URL = "https://duxqgefxnyrnlymsauso.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1eHFnZWZ4bnlybmx5bXNhdXNvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODk0MDEzMCwiZXhwIjoyMDc0NTE2MTMwfQ.QuP7Da1N6oi0D7ZoRMAASkJ8Z24NfZjsmCAlHj5OxqQ"

if not all([SUPABASE_URL, SUPABASE_KEY]):
    raise EnvironmentError("Failed to load database environment variables")

def get_db(request: Request) -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
