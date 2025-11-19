from pydantic import BaseModel, EmailStr

class ProfileModel(BaseModel):
    class Profile(BaseModel):
        id: str
        username: str
        email: EmailStr
        created_at: str | None = None

    class Edit(BaseModel):
        username: str
    