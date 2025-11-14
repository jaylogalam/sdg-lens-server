from fastapi import APIRouter, Request
from core.dependencies import GetDB, GetDBAdmin
# from services.admin_services import AdminServices
# from models.admin_models import AdminModel

router = APIRouter(
    prefix="/admin"
)

@router.post("/create_user")
def create_user(request: Request, db: GetDB):
    ...

@router.get("/read_user")
def read_user(request: Request, db: GetDB):
    ...

@router.put("/update_user")
def update_user(request: Request, db: GetDB):
    ...

@router.delete("/delete_user")
def delete_user(request: Request, db: GetDB):
    ...

