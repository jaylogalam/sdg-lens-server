from fastapi import Request, Response, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Callable, Awaitable
from core import Secrets
import jwt

security = HTTPBearer()

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
            SUPABASE_JWT = Secrets.SUPABASE_JWT
            if not SUPABASE_JWT:
                raise ValueError("Missing JWT credentials in environment variables")
            
            token = creds.credentials
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, SUPABASE_JWT, algorithms=["HS256"], options={"verify_aud": False})
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
        except jwt.PyJWKError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
