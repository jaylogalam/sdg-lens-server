from fastapi import APIRouter, Request
from db.dependencies import GetDB, GetUID
from core.limiter import limiter
from services.auth_services import AuthServices
from models import AuthModel
from utils.logs import create_log # type: ignore

router = APIRouter(
    prefix="/auth"
)
    
@router.post("/signup")
@limiter.limit("1/second") # type: ignore
def signup(request: Request, creds: AuthModel.Signup, db: GetDB):
    try:
        response = AuthServices.Signup.with_password(
            db=db,
            username=creds.username,
            email=creds.email,
            password=creds.password
        )
        return response
    
    except Exception as e:
        create_log(
            type='ERROR',
            description='auth: signup failed',
            user_id="anon",
            endpoint="/auth/signup",
            error=str(e)
        )
        return {"error": str(e)}

@router.post("/login")
@limiter.limit("1/second") # type: ignore
def login(request: Request, creds: AuthModel.Login, db: GetDB):
    try:
        auth_response = AuthServices.Login.with_password(
            db=db,
            email=creds.email,
            password=creds.password
        )
        
        return auth_response
        
    except Exception as e:
        create_log(
            type='ERROR',
            description='auth: login failed',
            user_id="anon",
            endpoint="/auth/login",
            error=str(e)
        )
        return {"error": str(e)}

@router.post("/logout")
@limiter.limit("1/second") # type: ignore
def logout(request: Request, db: GetDB, uid: GetUID):
    try:
        response = AuthServices.Logout.logout(db)
        create_log(
            type='LOG',
            description='user: logged out',
            user_id=uid,
            endpoint="/auth/logout",
        )

        return response
        
    except Exception as e:
        create_log(
            type='ERROR',
            description='auth: logout failed',
            user_id=uid,
            endpoint="/auth/logout",
            error=str(e)
        )
        return {"error": str(e)}