from fastapi import APIRouter, Request
from core.dependencies import GetClassifier, GetUser
from core import limiter
from services import AnalyzeServices
from models import AnalyzeModel

router = APIRouter(
    prefix="/analyze"
)
    
@router.get("")
@limiter.limit("1/second") # type: ignore
def analyze_text(
    request: Request,
    text: AnalyzeModel.Text,
    classifier: GetClassifier,
    user: GetUser
):
    try:
        return AnalyzeServices.analyze_text(
            text_input=text.text,
            classifier=classifier
        )
        
    except Exception as e:
        return {"error": str(e)}