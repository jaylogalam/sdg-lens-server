from fastapi import APIRouter, Request
from core import Dependencies
from services import ProfileServices

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
def get_profile(request: Request, db: Dependencies.GetDB):
    try:
        response = ProfileServices.get_profile(db=db, user_id="some_user_id")
        return response
        
    except Exception as e:
        return {"error": str(e)}
    