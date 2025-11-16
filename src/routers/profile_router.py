from fastapi import APIRouter, Request
from db.dependencies import GetDB
from services.profile_services import ProfileServices
from core.limiter import limiter

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
@limiter.limit("5/second") # type: ignore
def get_profile(request: Request, db: GetDB):
    try:
        response = ProfileServices.get_profile_data(db)
        return response
        
    except Exception as e:
        return {"error": str(e)}