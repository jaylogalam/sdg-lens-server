from fastapi import Depends
from typing import Annotated, Any
from core import AuthMiddleware, Database
from supabase import Client

class Dependencies:
    GetUser = Annotated[dict[str, Any], Depends(AuthMiddleware.get_user)]
    GetDB = Annotated[Client, Depends(Database.get_db)]