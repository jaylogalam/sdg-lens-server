from fastapi import APIRouter, Request
from db.dependencies import GetDBAdmin
from core.limiter import limiter
from services.admin_services import AdminServices
from models.admin_models import AdminModel

router = APIRouter(
    prefix="/admin"
)

@router.post("/create_user")
@limiter.limit("1/second") # type: ignore
def create_user(request: Request, db: GetDBAdmin, data: AdminModel.NewUser):
    try:
        response = AdminServices.create_user(
            db=db,
            email=data.email,
            password=data.password,
            user_metadata=data.user_metadata
        )
        return response
        
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.get("/read_users")
@limiter.limit("1/second") # type: ignore
def read_user(request: Request, db: GetDBAdmin):
    try:
        response = AdminServices.read_user(db)
        return response
    
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.put("/update_user")
@limiter.limit("1/second") # type: ignore
def update_user(request: Request, db: GetDBAdmin, id: str, data: dict[str, str]):
    try:
        response = AdminServices.update_user(db, id, data)
        return response
        
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.delete("/delete_user")
@limiter.limit("1/second") # type: ignore
def delete_user(request: Request, db: GetDBAdmin, id: str):
    try:
        response = AdminServices.delete_user(db, id)
        return response
        
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

