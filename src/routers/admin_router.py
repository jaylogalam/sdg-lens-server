from fastapi import APIRouter, Request
from db.dependencies import GetDBAdmin, GetUID
from core.limiter import limiter
from services.admin_services import AdminServices
from models.admin_models import AdminModel
from utils.logs import create_log # type: ignore

router = APIRouter(
    prefix="/admin"
)

@router.post("/create_user")
@limiter.limit("1/second") # type: ignore
def create_user(request: Request, db: GetDBAdmin, data: AdminModel.NewUser, uid: GetUID):
    try:
        response = AdminServices.create_user(
            db=db,
            email=data.email,
            password=data.password,
            username=data.username,
        )
        
        create_log(
            type='LOG',
            description='admin: created new user',
            user_id=uid,
            endpoint="/admin/create_user",
            data=dict(data)
        )
        return response
        
    except Exception as e:
        create_log(
            type='ERROR',
            description='admin: failed to create user',
            user_id=uid,
            endpoint="/admin/create_user",
            error=str(e)
        )
        raise ValueError(f"An error occurred: {str(e)}")

@router.get("/read_user/{user_id}")
@limiter.limit("1/second") # type: ignore
def read_user(request: Request, db: GetDBAdmin, user_id: str, uid: GetUID):
    try:
        response = AdminServices.read_user(db, user_id)
        return response
    
    except Exception as e:
        raise ValueError(f"Error reading users: {str(e)}")

@router.get("/read_users")
@limiter.limit("1/second") # type: ignore
def read_users(request: Request, db: GetDBAdmin, uid: GetUID):
    try:
        response = AdminServices.read_users(db)
        create_log(
            type='LOG',
            description='admin: read users',
            user_id=uid,
            endpoint="/admin/read_users",
        )
        return response
    
    except Exception as e:
        create_log(
            type='ERROR',
            description='admin: failed to read users',
            user_id=uid,
            endpoint="/admin/read_users",
            error=str(e)
        )
        raise ValueError(f"Error reading users: {str(e)}")

@router.get("/read_admins")
@limiter.limit("1/second") # type: ignore
def read_admins(request: Request, db: GetDBAdmin, uid: GetUID):
    try:
        response = AdminServices.read_admins(db)
        create_log(
            type='LOG',
            description='admin: read admins',
            user_id=uid,
            endpoint="/admin/read_admins",
        )
        return response
    
    except Exception as e:
        create_log(
            type='ERROR',
            description='admin: failed to read users',
            user_id=uid,
            endpoint="/admin/read_users",
            error=str(e)
        )
        raise ValueError(f"Error reading users: {str(e)}")
    
@router.put("/update_user/{user_id}")
@limiter.limit("1/second") # type: ignore
def update_user(request: Request, db: GetDBAdmin, user_id: str, data: dict[str, str], uid: GetUID):
    try:
        response = AdminServices.update_user(
            db=db,
            id=user_id,
            username=data.get('username'), # type: ignore
            app_role=data.get('app_role')  # type: ignore
        )
        create_log(
            type='LOG',
            description=f'admin: updated user, id={user_id}',
            user_id=uid,
            endpoint="/admin/update_user",
            data=data
        )
        return response
        
    except Exception as e:
        create_log(
            type='ERROR',
            description=f'admin: failed to update user, id={user_id}',
            user_id=uid,
            endpoint="/admin/update_user",
            error=str(e)
        )
        raise ValueError(f"Error updating user: {str(e)}")

@router.delete("/delete_user/{user_id}")
@limiter.limit("1/second") # type: ignore
def delete_user(request: Request, db: GetDBAdmin, user_id: str, uid: GetUID):
    try:
        response = AdminServices.delete_user(db, user_id)
        create_log(
            type='LOG',
            description=f'admin: deleted user, id={user_id}',
            user_id=uid,
            endpoint="/admin/delete_user",
        )
        return response
        
    except Exception as e:
        create_log(
            type='ERROR',
            description=f'admin: failed to update user, id={user_id}',
            user_id=uid,
            endpoint="/admin/delete_user",
            error=str(e)
        )
        raise ValueError(f"Error deleting user: {str(e)}")

