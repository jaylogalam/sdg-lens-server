from fastapi import APIRouter, Request
from core.dependencies import GetUser
from core.limiter import limiter
from services.analyze_services import AnalyzeServices
from models import AnalyzeModel

router = APIRouter(
    prefix="/analyze"
)
    
@router.get("")
@limiter.limit("1/second") # type: ignore
def analyze_text(
    request: Request,
    text: AnalyzeModel.Text,
    user: GetUser
):
    try:
        return AnalyzeServices.analyze_text(text.text)
        
    except Exception as e:
        return {"error": str(e)}