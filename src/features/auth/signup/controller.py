from fastapi import APIRouter, Response
from .model import SignupModel
from .services import create_user_with_email_password

router = APIRouter(
      prefix="/signup"
)

@router.get("/password")
def signup_with_password(data: SignupModel):
    user = create_user_with_email_password(data.email, data.password)
    return user