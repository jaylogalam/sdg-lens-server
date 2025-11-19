from pydantic import BaseModel

class AdminModel:
    class NewUser(BaseModel):
        email: str
        password: str
        username: str