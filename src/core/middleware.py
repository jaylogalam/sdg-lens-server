# core/middleware.py
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
    # Build origins safely
    _origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Only add CLIENT_URL if it is set and not empty
    if CLIENT_URL:
        _origins.append(CLIENT_URL)

    # You do NOT need to add "http://127.0.0.1:8000" (backend URL) here;
    # CORS cares about the FRONTEND origin only.
    
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