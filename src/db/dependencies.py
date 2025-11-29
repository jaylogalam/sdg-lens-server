# db/dependencies.py
from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional
from supabase import Client

from db.supabase import get_db, get_db_admin, get_id, get_token


GetDB = Annotated[Client, Depends(get_db)]
GetDBAdmin = Annotated[Client, Depends(get_db_admin)]


def _get_uid_required(token: str = Depends(get_token)) -> str:
    """
    Must be logged in. Raises 401 if there is no valid user id.
    """
    user_id = get_id(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user_id


def _get_uid_optional(token: str = Depends(get_token)) -> Optional[str]:
    """
    Optional auth: returns user id if logged in, otherwise None.
    """
    return get_id(token)


GetUID = Annotated[str, Depends(_get_uid_required)]
GetUIDOptional = Annotated[Optional[str], Depends(_get_uid_optional)]
