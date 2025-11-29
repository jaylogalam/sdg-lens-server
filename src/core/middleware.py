from fastapi import FastAPI
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
    # Base allowed origins (local dev)
    _origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Optionally add CLIENT_URL from env if it exists
    if CLIENT_URL:
        _origins.append(CLIENT_URL)

    Settings: dict[str, Any] = {
        "allow_origins": _origins,
        "allow_credentials": True,   # needed for cookies (withCredentials: true)
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "expose_headers": ["Content-Disposition"],
    }

    @classmethod
    def register(cls, app: FastAPI):
        app.add_middleware(CORSMiddleware, **cls.Settings)




# from fastapi import FastAPI
# from fastapi.security import HTTPBearer
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Any
# from core.secrets import CLIENT_URL

# security = HTTPBearer()

# class Middleware:
#     @staticmethod
#     def register(app: FastAPI):
#         CorsMiddleware.register(app)

# class CorsMiddleware:
#     _origins: list[Any] = [
#         CLIENT_URL,
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#         "http://127.0.0.1:8000"
#     ]
    
#     Settings: dict[str, Any] = {
#         "allow_origins": _origins, 
#         "allow_credentials": True,
#         "allow_methods": ["*"],
#         "allow_headers": ["*"],
#         "expose_headers": ["Content-Disposition"], 
#     }

#     @classmethod
#     def register(cls, app: FastAPI):
#         app.add_middleware(CORSMiddleware, **cls.Settings)