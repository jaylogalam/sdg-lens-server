from fastapi import APIRouter, Request
from typing import Annotated
from fastapi.params import Depends
from database import get_db, Client
from core import limiter
from services import AuthServices
from models import AuthModel

router = APIRouter(
    prefix="/auth"
)
    
@router.post("/signup")
@limiter.limit("1/second") # type: ignore
def test(request: Request, creds: AuthModel.Signup, db: Annotated[Client, Depends(get_db)]):
    try:
        return AuthServices.Signup.with_password(
            db=db,
            username=creds.username,
            email=creds.email,
            password=creds.password
        )
        
    except Exception as e:
        return {"error": str(e)}