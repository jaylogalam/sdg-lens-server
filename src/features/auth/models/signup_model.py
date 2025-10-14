from pydantic import BaseModel

class SignupModel(BaseModel):
    username: str
    email: str
    password: str

