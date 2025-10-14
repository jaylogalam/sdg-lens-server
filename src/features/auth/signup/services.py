from ....database import db
from .model import SignupModel

def create_user_with_email_password(email: str, password: str):
    auth_response = db.auth.sign_up(
        {"email": email, "password": password}
    )
    
    user = auth_response.user

    if not user:
        return "not user error"
    
    return user