from fastapi import APIRouter, Request
from core.dependencies import GetUser, GetDB
from services.profile_services import ProfileServices

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
def get_profile(request: Request, user: GetUser, db: GetDB):
    try:
        id = user.get("sub")
        if not id:
            raise ValueError("No id")
        response = ProfileServices.get_profile_data(db, id)
        # return response
        return response
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/admin")
def get_all_profiles(request: Request, user: GetUser, db: GetDB):
    try:
        id = user.get("sub")
        if not id:
            raise ValueError("No id")

        response = ProfileServices.get_profile_data_admin(db, id)
        return response

    except Exception as e:
        return {"error": str(e)}
    