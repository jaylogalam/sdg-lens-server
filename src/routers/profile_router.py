from fastapi import APIRouter, Request
from fastapi.params import Depends
from typing import Annotated
from database import get_db, Client
from services import ProfileServices
from services import AuthServices

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
def get_profile(request: Request, db: Annotated[Client, Depends(get_db)]):
    try:
        response = ProfileServices.get_profile(db=db, user_id="some_user_id")
        return response
        
    except Exception as e:
        return {"error": str(e)}
    