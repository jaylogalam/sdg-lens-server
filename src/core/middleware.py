from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from core.secrets import CLIENT_URL

security = HTTPBearer()

class Middleware:
    @staticmethod
    def register(app: FastAPI):
        CorsMiddleware.register(app)

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
    def get_token(request: Request):
        try:
            token = request.cookies.get("access_token")

            if token and token.startswith('Bearer '):
                token = token[7:]

            if not token:
                return ""

            return token
        
        except Exception as e:
            raise Exception(f"Error getting user: {e}")