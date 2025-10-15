from fastapi import APIRouter
from services import AuthServices
from models import SignupModel

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
def test(req: SignupModel):
    # Add user to database
    AuthServices.Signup.with_password(
        email=req.email,
        password=req.password
    )