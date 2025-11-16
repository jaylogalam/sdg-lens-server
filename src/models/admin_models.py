from pydantic import BaseModel

class AdminModel:
    class NewUser(BaseModel):
        email: str
        password: str
        user_metadata: dict[str, str]