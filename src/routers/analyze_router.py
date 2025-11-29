# routes/analyze_routes.py
import traceback
from fastapi import APIRouter, Request, HTTPException
from core.limiter import limiter
from services.analyze_services import AnalyzeServices
from models import AnalyzeModel
from db.dependencies import GetUID, GetDB, GetUIDOptional
from utils.logs import create_log  # type: ignore

router = APIRouter(prefix="/analyze")


@router.post("")
@limiter.limit("1/second")  # type: ignore
def analyze_text(
    request: Request,
    payload: AnalyzeModel.Text,
    db: GetDB,
    uid: GetUIDOptional,  # can be None now
):
    try:
        # uid may be None for guests; AnalyzeServices will handle that
        response = AnalyzeServices.analyze_text(db, payload.text, uid)

        if hasattr(payload, "model_dump"):
            payload_dict = payload.model_dump()
        else:
            payload_dict = payload.dict()

        log_user_id = uid or "anonymous"

        create_log(
            type="LOG",
            description="user: analyze document",
            user_id=log_user_id,
            endpoint="/analyze",
            data={"payload": payload_dict, "results": response},
        )
        return response

    except Exception as e:
        print("ERROR IN /analyze:", e)
        traceback.print_exc()

        log_user_id = uid or "anonymous"

        create_log(
            type="ERR",
            description="user: analyze document failed",
            user_id=log_user_id,
            endpoint="/analyze",
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
@limiter.limit("5/second")  # type: ignore
def get_history(
    request: Request,
    db: GetDB,
    uid: GetUID,  # must be logged in to see history
):
    try:
        response = AnalyzeServices.get_history(db, uid)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
