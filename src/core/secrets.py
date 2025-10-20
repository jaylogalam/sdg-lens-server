from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_URL = os.getenv('CLIENT_URL')
PIPELINE_URL = os.getenv('PIPELINE_URL')
PIPELINE_KEY = os.getenv('PIPELINE_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_KEY_ADMIN = os.getenv('SUPABASE_KEY_ADMIN')
SUPABASE_JWT = os.getenv('SUPABASE_JWT')