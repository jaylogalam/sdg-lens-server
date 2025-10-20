from fastapi import APIRouter, Request
from core.dependencies import GetUser, GetDBAdmin
from services.profile_services import ProfileServices

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
def get_profile(request: Request, user: GetUser, db: GetDBAdmin):
    try:
        response = ProfileServices.get_profile_data(db, user.id)
        return response
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/admin")
def get_all_profiles(request: Request, user: GetUser, db: GetDBAdmin):
    try:
        response = ProfileServices.get_profile_data_admin(db, user.id)
        return response

    except Exception as e:
        return {"error": str(e)}
    