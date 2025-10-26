from fastapi import APIRouter, Request
from core.dependencies import GetDB, GetDBAdmin
from core.limiter import limiter
from services.auth_services import AuthServices
from models import AuthModel

router = APIRouter(
    prefix="/auth"
)
    
@router.post("/signup")
@limiter.limit("1/second") # type: ignore
def signup(request: Request, creds: AuthModel.Signup, db: GetDB, admin: GetDBAdmin):
    try:
        return AuthServices.Signup.with_password(
            db=db,
            admin=admin,
            username=creds.username,
            email=creds.email,
            password=creds.password
        )
        
    except Exception as e:
        return {"error": str(e)}

@router.post("/login")
@limiter.limit("1/second") # type: ignore
def login(request: Request, creds: AuthModel.Login, db: GetDB, admin: GetDBAdmin):
    try:
        auth_response = AuthServices.Login.with_password(
            db=db,
            admin=admin,
            email=creds.email,
            password=creds.password
        )

        return auth_response
        
    except Exception as e:
        return {"error": str(e)}

@router.post("/logout")
@limiter.limit("1/second") # type: ignore
def logout(request: Request, db: GetDB):
    try:
        return AuthServices.Logout.logout(db)
        
    except Exception as e:
        return {"error": str(e)}