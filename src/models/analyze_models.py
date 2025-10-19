from pydantic import BaseModel

class AnalyzeModel:
    class Text(BaseModel):
        text: str