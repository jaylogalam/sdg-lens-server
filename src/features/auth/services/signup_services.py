# Supabase connection
from supabase import create_client, Client
SUPABASE_URL = "https://duxqgefxnyrnlymsauso.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1eHFnZWZ4bnlybmx5bXNhdXNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5NDAxMzAsImV4cCI6MjA3NDUxNjEzMH0.KpKohNP5fOlcGeC2s2rdArCmsTcZHb9CaX7ez-3Eh0A"
db: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Model
from pydantic import BaseModel
class SignupModel(BaseModel):
    username: str
    email: str
    password: str

def signup_with_password(data: SignupModel):
    # Step 1: Sign up user in Supabase Auth
    auth_response = db.auth.sign_up(
        {"email": data.email, "password": data.password}
    )
    user = auth_response.user

    if not user:
        return "not user error"

    # Step 2: Create profile record
    profile = {
        "id": user.id,
        "username": data.username,
    }

    profile_response = db.table("profiles").insert(profile).execute()
    if profile_response.error:
        return "profile creation error"

    return "Success"

if __name__ == "__main__":
    data = SignupModel(
        username="testuser",
        email="testuser@gmail.com",
        password="123456"
    )
    signup_with_password(data)