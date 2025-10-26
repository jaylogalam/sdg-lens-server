from fastapi import APIRouter, Request
from core.dependencies import GetDB
from services.profile_services import ProfileServices

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
def get_profile(request: Request, db: GetDB):
    try:
        response = ProfileServices.get_profile_data(db)
        return response
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/admin")
def get_all_profiles(request: Request, db: GetDB):
    try:
        response = ProfileServices.get_profile_data_admin(db)
        return response

    except Exception as e:
        return {"error": str(e)}
    