from fastapi import APIRouter, Request
from services.auth import AuthServices
from models.auth import SignupModel

router = APIRouter(
    prefix="/signup"
)

@router.post("/")
def signup(request: SignupModel):
    response = AuthServices.Signup.with_password(
        email = request.email,
        password = request.password
    )
    
    return response

@router.get("/test")
def test(request: Request):

    return request