from fastapi import APIRouter, Request
from core.dependencies import GetDB, GetDBAdmin
from services.profile_services import ProfileServices
from models.profile_models import ProfileModel

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

@router.post("/edit_username")
def edit_username(request: Request, profile: ProfileModel.Edit, db: GetDB, admin: GetDBAdmin):
    try:
        response = ProfileServices.edit_username(
            db = db,
            admin = db,
            name = profile.username
        )
        
        return response

    except Exception as e:
        return {"error": str(e)}
