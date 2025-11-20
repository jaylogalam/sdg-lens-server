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
            username=data.username,
        )
        
        return response
        
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.get("/read_user/{user_id}")
@limiter.limit("1/second") # type: ignore
def read_user(request: Request, db: GetDBAdmin, user_id: str):
    try:
        response = AdminServices.read_user(db, user_id)
        return response
    
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.get("/read_users")
@limiter.limit("1/second") # type: ignore
def read_users(request: Request, db: GetDBAdmin):
    try:
        response = AdminServices.read_users(db)
        return response
    
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.put("/update_user/{user_id}")
@limiter.limit("1/second") # type: ignore
def update_user(request: Request, db: GetDBAdmin, user_id: str, data: dict[str, str]):
    try:
        print(data)
        response = AdminServices.update_user(
            db=db,
            id=user_id,
            username=data.get('username'),
            app_role=data.get('app_role')
        )
        return response
        
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.delete("/delete_user/{user_id}")
@limiter.limit("1/second") # type: ignore
def delete_user(request: Request, db: GetDBAdmin, user_id: str):
    try:
        response = AdminServices.delete_user(db, user_id)
        return response
        
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

