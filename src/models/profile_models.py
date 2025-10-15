from pydantic import BaseModel

class ProfileModel(BaseModel):
    id: str
    username: str
    created_at: str | None = None