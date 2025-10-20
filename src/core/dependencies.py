from fastapi import Depends
from typing import Annotated, Any
from supabase import Client

from core.middleware import AuthMiddleware
from core.database import Database

GetUser = Annotated[Any, Depends(AuthMiddleware.get_user)]
GetDB = Annotated[Client, Depends(Database.get_db)]
GetDBAdmin = Annotated[Client, Depends(Database.get_db_admin)]