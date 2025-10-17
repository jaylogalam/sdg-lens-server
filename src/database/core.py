from fastapi import Request
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not all([SUPABASE_URL, SUPABASE_KEY]):
    raise EnvironmentError("Failed to load database environment variables")

def get_db(request: Request) -> Client:
    db = create_client(SUPABASE_URL, SUPABASE_KEY)
    token = request.cookies.get("sb-access-token")
    if token:
        db.auth.set_session(access_token=token, refresh_token=token)
    return db