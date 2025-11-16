from fastapi import Depends
from typing import Annotated
from supabase import Client
from db.supabase import get_db, get_db_admin

GetDB = Annotated[Client, Depends(get_db)]
GetDBAdmin = Annotated[Client, Depends(get_db_admin)]
