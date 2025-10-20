from fastapi import FastAPI, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable, Awaitable, Any
from core.secrets import CLIENT_URL, SUPABASE_JWT
from core.database import Database

security = HTTPBearer()

class Middleware:
    @staticmethod
    def register(app: FastAPI):
        CorsMiddleware.register(app)
        AuthMiddleware.register(app)

class CorsMiddleware:
    _origins: list[Any] = [
        CLIENT_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000"
    ]
    
    Settings: dict[str, Any] = {
        "allow_origins": _origins, 
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "expose_headers": ["Content-Disposition"], 
    }

    @classmethod
    def register(cls, app: FastAPI):
        app.add_middleware(CORSMiddleware, **cls.Settings)

class AuthMiddleware:
    @staticmethod
    async def __call__(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        print(f"Running middleware...\n")
        token = request.cookies.get('access_token')
        print(f"Login access token: {token}\n")
        
        if token and token.startswith('Bearer '):
            token = token[7:]
            request.headers.__dict__['_list'].append(
                (b"authorization", f"Bearer {token}".encode())
            )

        response = await call_next(request)
        print("Success!")
        return response

    @staticmethod
    def get_user(creds: HTTPAuthorizationCredentials = Depends(security)):
        try:
            print("Retrieving user...\n")
            token = creds.credentials
            print(f"Get user access token: {token}\n")

            db = Database.get_db()
            
            print("Retrieving user claims...\n")
            user = db.auth.get_claims(SUPABASE_JWT)
            if not user:
                raise Exception("Cannot retrieve user!\n")

            print("Retrieving user id...\n")
            user_id = user.get("sub")
            
            print("Successfully retrieved user\n")
            return user_id
        
        except Exception as e:
            raise Exception(f"Error getting user: {e}")

    @staticmethod
    def register(app: FastAPI):
        app.middleware("http")(AuthMiddleware())

