from fastapi import Depends
from typing import Annotated
from supabase import Client

from core.database import Database

GetDB = Annotated[Client, Depends(Database.get_db)]
GetDBAdmin = Annotated[Client, Depends(Database.get_db_admin)]