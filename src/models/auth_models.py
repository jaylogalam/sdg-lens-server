from pydantic import BaseModel, EmailStr

class AuthModel:
    class Signup(BaseModel):
        username: str
        email: EmailStr
        password: str