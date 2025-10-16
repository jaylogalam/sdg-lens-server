from postgrest.exceptions import APIError
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
def signup(request: Request, db: Annotated[Client, Depends(get_db)]):
    creds: AuthModel.Signup = AuthModel.Signup.model_validate(request.json())
    user = AuthServices.Signup.with_password(creds, db)
    # ProfileServices.initialize_profile(user, db)
    
    return user
    
@router.get("/test")
@limiter.limit("1/second") # type: ignore
def test(request: Request, creds: AuthModel.Signup, db: Annotated[Client, Depends(get_db)]):
    try:
        AuthServices.Signup.with_password(creds, db)
    except APIError as e:
        if getattr(e, "code", None) == "23505":
            return {"error": "Username already exists"}
        
        return {"error": str(e)}

    # 23505