from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_JWT = os.getenv('SUPABASE_JWT')
security = HTTPBearer()

class AuthMiddleware:
    @staticmethod
    async def __call__(request: Request, call_next):
        token = request.cookies.get('access_token')
        if token and token.startswith('Bearer '):
            token = token[7:]  # Remove 'Bearer ' prefix
            request.headers.__dict__['list'].append(
                (b"authorization", f"Bearer {token}".encode())
            )

        response = await call_next(request)
        return response
    
    def get_user(creds: HTTPAuthorizationCredentials = Depends(security)):
        try:
            token = creds.credentials
            if token.startswith('Bearer '):
                token = token[7:]  # Remove 'Bearer ' prefix
            payload = jwt.decode(token, SUPABASE_JWT, algorithms=["HS256"], options={"verify_aud": False})
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
        except jwt.PyJWKError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
