# routes/analyze_routes.py (or similar)
from fastapi import APIRouter, Request, HTTPException
from core.limiter import limiter
from services.analyze_services import AnalyzeServices
from models import AnalyzeModel

router = APIRouter(prefix="/analyze")

@router.post("")
@limiter.limit("1/second")  # type: ignore
def analyze_text(
    request: Request,
    payload: AnalyzeModel.Text,
):
    try:
        return AnalyzeServices.analyze_text(payload.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
