from fastapi import APIRouter, Request
from typing import Annotated, Any
from fastapi.params import Depends
from database import get_db, Client
from core import AuthMiddleware, limiter
from services import AuthServices
from models import AuthModel

router = APIRouter(
    prefix="/auth"
)
    
@router.post("/signup")
@limiter.limit("1/second") # type: ignore
def signup(request: Request, creds: AuthModel.Signup, db: Annotated[Client, Depends(get_db)]):
    try:
        return AuthServices.Signup.with_password(
            db=db,
            username=creds.username,
            email=creds.email,
            password=creds.password
        )
        
    except Exception as e:
        return {"error": str(e)}

@router.post("/login")
@limiter.limit("1/second") # type: ignore
def login(request: Request, creds: AuthModel.Login, db: Annotated[Client, Depends(get_db)]):
    try:
        auth_response = AuthServices.Login.with_password(
            db=db,
            email=creds.email,
            password=creds.password
        )

        return auth_response
        
    except Exception:
        return {"error": "Incorrect password"}

@router.post("/logout")
@limiter.limit("1/second") # type: ignore
def logout(request: Request, db: Annotated[Client, Depends(get_db)]):
    try:
        return AuthServices.Logout.logout(db)
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/user")
def get_current_user(
    request: Request,
    user: Annotated[dict[str, Any], Depends(AuthMiddleware.get_user)],
    db: Annotated[Client, Depends(get_db)]
):
    try:
        return user
        
    except Exception as e:
        return {"error": str(e)}