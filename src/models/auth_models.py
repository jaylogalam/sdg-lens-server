from pydantic import BaseModel, EmailStr

class AuthModel:
    class Signup(BaseModel):
        username: str
        email: EmailStr
        password: str

    class Login(BaseModel):
        email: EmailStr
        password: str