
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any
from datetime import datetime, date

class HistoryModel:
    class UserHistoryRequest(BaseModel):
        email: EmailStr
        start_date: date
        end_date: date

    class HistoryItem(BaseModel):
        action: str
        item: str
        details: Dict[str, Any] | None = None
        created_at: datetime

    class UserHistoryResponse(BaseModel):
        email: EmailStr
        history: List[HistoryItem] # type: ignore
