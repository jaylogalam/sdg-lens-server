from fastapi import FastAPI, Request, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable, Awaitable, Any
from core.secrets import CLIENT_URL
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
        print(f"Running middleware...")
        token = request.cookies.get('access_token')
        
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
            print("Retrieving user...")
            token = creds.credentials

            db = Database.get_db()
            
            user = db.auth.get_user(token)
            if not user:
                raise Exception("Cannot retrieve user!\n")

            return user.user
        
        except Exception as e:
            raise Exception(f"Error getting user: {e}")

    @staticmethod
    def register(app: FastAPI):
        app.middleware("http")(AuthMiddleware())

