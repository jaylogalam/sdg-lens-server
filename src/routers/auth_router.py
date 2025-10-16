from fastapi import APIRouter, Request
from typing import Annotated
from fastapi.params import Depends
from database import get_db, Client
from core import limiter
from services import AuthServices
from models import AuthModel

router = APIRouter(
    prefix="/signup"
)

@router.post("")
@limiter.limit("1/second") # type: ignore
def signup(request: Request, creds: AuthModel.Signup, db: Annotated[Client, Depends(get_db)]):
    AuthServices.Signup.with_password(creds, db)
    return {"message": "User created successfully"}
    
@router.get("/test")
@limiter.limit("1/second") # type: ignore
def test(request: Request, creds: AuthModel.Signup, db: Annotated[Client, Depends(get_db)]):
    AuthServices.Signup.with_password(creds, db)
    return {"message": "User created successfully"}