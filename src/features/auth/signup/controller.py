from fastapi import APIRouter
from .model import SignupModel
from .services import signup_using_password

router = APIRouter(
      prefix="/signup"
)

@router.get("/password")
def signup_with_password():
    # data: SignupModel
    data = SignupModel(
        email="test@gmail.com",
        password="12345"
    )

    return data