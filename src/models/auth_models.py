from pydantic import BaseModel, EmailStr
from datetime import datetime

class AuthModel:
    class InitProfile(BaseModel):
        id: str
        created_at: datetime
        username: str
        
    class Signup(BaseModel):
        username: str
        email: EmailStr
        password: str