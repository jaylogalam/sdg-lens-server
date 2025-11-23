# routes/analyze_routes.py
from fastapi import APIRouter, Request, HTTPException
from core.limiter import limiter
from services.analyze_services import AnalyzeServices
from models import AnalyzeModel
from db.dependencies import GetUID, GetDB
from utils.logs import create_log  # type: ignore

router = APIRouter(prefix="/analyze")

@router.post("")
@limiter.limit("1/second")  # type: ignore
def analyze_text(  # type: ignore
    request: Request,
    payload: AnalyzeModel.Text,
    db: GetDB,
    uid: GetUID,
):
    try:
        response = AnalyzeServices.analyze_text(db, payload.text, uid)  # type: ignore
        create_log(
            type="LOG",
            description="user: analyze document",
            user_id=uid,
            endpoint="/analyze",
            data={"payload": dict(payload), "results": response},
        )
        return response  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
@limiter.limit("5/second")  # type: ignore
def get_history(
    request: Request,
    db: GetDB,
    uid: GetUID,   # ✅ get logged-in user id from dependency
):
    try:
        response = AnalyzeServices.get_history(db, uid)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
