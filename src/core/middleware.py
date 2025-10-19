from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable, Awaitable, Any
from core.secrets import CLIENT_URL, SUPABASE_JWT
import jwt

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
        token = request.cookies.get('access_token')
        if token and token.startswith('Bearer '):
            token = token[7:]
            request.headers.__dict__['_list'].append(
                (b"authorization", f"Bearer {token}".encode())
            )

        response = await call_next(request)
        return response

    @staticmethod
    def get_user(creds: HTTPAuthorizationCredentials = Depends(security)):
        try:
            JWT = SUPABASE_JWT
            if not JWT:
                raise ValueError("Missing JWT credentials in environment variables")
            
            token = creds.credentials
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, JWT, algorithms=["HS256"], options={"verify_aud": False})
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
        except jwt.PyJWKError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

    @staticmethod
    def register(app: FastAPI):
        app.middleware("http")(AuthMiddleware())

