from dotenv import load_dotenv
import os

load_dotenv()

class Secrets:
    CLIENT_URL = os.getenv('CLIENT_URL')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_JWT = os.getenv('SUPABASE_JWT')