from fastapi import Depends, Request
from supabase import create_client, Client
from supabase.client import ClientOptions
from core.secrets import SUPABASE_URL, SUPABASE_KEY, SUPABASE_KEY_ADMIN
from typing import Annotated, Any
import jwt

def get_token(request: Request):
    token = request.cookies.get("access_token")
    if token and token.startswith('Bearer '):
        return token[7:]
    return ""
    
GetToken = Annotated[Any, Depends(get_token)]

if not SUPABASE_URL or not SUPABASE_KEY or not SUPABASE_KEY_ADMIN:
    raise ValueError("Missing Supabase credentials in environment variables")

def get_db(token: GetToken) -> Client:    
    if not token:   
        return create_client(SUPABASE_URL, SUPABASE_KEY)

    return create_client(SUPABASE_URL, SUPABASE_KEY,
        options=ClientOptions(
            headers={"Authorization": f"Bearer {token}"}
        )
    )

def get_db_admin(token: GetToken):
    role = get_role(token)
    if role != "admin":
        raise ValueError("Unauthorized")
    
    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY_ADMIN,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        )
    )

def get_role(token: str):
    decoded_payload = jwt.decode(
        jwt=token,
        algorithms=["HS256"],
        options={
            "verify_signature": False,
            "verify_exp": True
        }
    )

    user_metadata = decoded_payload.get("user_metadata", {})
    print(user_metadata.get("app_role"))
    return user_metadata.get("app_role")

def db_admin():
    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY_ADMIN,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        )
    )