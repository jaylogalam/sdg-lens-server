from pydantic import BaseModel

class AuthModel:
    class Signup(BaseModel):
        email: str
        password: str