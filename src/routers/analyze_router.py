from fastapi import APIRouter, Request
from core.limiter import limiter
from services.analyze_services import AnalyzeServices
from models.analyze_models import AnalyzeModel

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"]
)

@router.post("/")
@limiter.limit("1/second")
def analyze_text(request: Request, payload: AnalyzeModel):
    """
    Analyze text locally (no external AI).
    """
    result = AnalyzeServices.analyze_text(payload.text)
    return {
        "message": "Text analyzed successfully",
        "data": result
    }
