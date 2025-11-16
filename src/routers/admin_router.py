from fastapi import APIRouter, Request
from db.dependencies import GetDBAdmin
from core.limiter import limiter
from services.admin_services import AdminServices

router = APIRouter(
    prefix="/admin"
)

@router.post("/create_user")
@limiter.limit("1/second") # type: ignore
def create_user(request: Request, db: GetDBAdmin):
    ...

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
def update_user(request: Request, db: GetDBAdmin):
    ...

@router.delete("/delete_user")
@limiter.limit("1/second") # type: ignore
def delete_user(request: Request, db: GetDBAdmin):
    ...

