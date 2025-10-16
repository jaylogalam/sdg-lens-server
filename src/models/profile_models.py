from pydantic import BaseModel, EmailStr

class ProfileModel(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_at: str | None = None
    