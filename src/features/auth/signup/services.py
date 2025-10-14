from database import db
from .model import SignupModel

def signup_using_password(data: SignupModel):
    # Step 1: Sign up user in Supabase Auth
    auth_response = db.auth.sign_up(
        {"email": data.email, "password": data.password}
    )
    user = auth_response.user

    if not user:
        return "not user error"
    
    return user