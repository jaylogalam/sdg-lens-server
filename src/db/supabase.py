# db/supabase.py
from fastapi import Depends, Request
from supabase import create_client, Client
from supabase.client import ClientOptions
from core.secrets import SUPABASE_URL, SUPABASE_KEY, SUPABASE_KEY_ADMIN
from typing import Annotated, Any, Optional
import jwt
from jwt import PyJWTError


def get_token(request: Request) -> str:
    """
    Read the access_token cookie, strip the 'Bearer ' prefix if present.
    Returns empty string if not logged in.
    """
    token = request.cookies.get("access_token")
    if token and token.startswith("Bearer "):
        return token[7:]
    return ""


GetToken = Annotated[Any, Depends(get_token)]


if not SUPABASE_URL or not SUPABASE_KEY or not SUPABASE_KEY_ADMIN:
    raise ValueError("Missing Supabase credentials in environment variables")


def get_db(token: GetToken) -> Client:
    """
    Create a Supabase client.
    - If no token -> anonymous client (public key).
    - If token present -> attach Authorization header.
    """
    if not token:
        return create_client(SUPABASE_URL, SUPABASE_KEY)

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
        options=ClientOptions(headers={"Authorization": f"Bearer {token}"}),
    )


def get_role(token: str) -> Optional[str]:
    """
    Decode the token and return app_role from user_metadata.
    Returns None if token is missing/invalid.
    """
    if not token:
        return None

    try:
        decoded_payload = jwt.decode(
            jwt=token,
            algorithms=["HS256"],
            options={
                "verify_signature": False,  # Supabase signs it; we just need metadata
                "verify_exp": True,
            },
        )
    except PyJWTError:
        return None

    user_metadata = decoded_payload.get("user_metadata", {}) or {}
    return user_metadata.get("app_role")


def get_db_admin(token: GetToken) -> Client:
    """
    Admin client – only for users with app_role=admin.
    """
    role = get_role(token)
    if role != "admin":
        raise ValueError("Unauthorized")

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY_ADMIN,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        ),
    )


def get_id(token: Optional[str]) -> Optional[str]:
    """
    Decode the token and return the user id (sub).
    Returns None if token is missing/invalid.
    """
    if not token:
        return None

    try:
        decoded_payload = jwt.decode(
            jwt=token,
            algorithms=["HS256"],
            options={
                "verify_signature": False,
                "verify_exp": True,
            },
        )
    except PyJWTError:
        return None

    return decoded_payload.get("sub")


def db_admin() -> Client:
    """
    Raw admin client without any auth check.
    Only use this internally / carefully.
    """
    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY_ADMIN,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        ),
    )
