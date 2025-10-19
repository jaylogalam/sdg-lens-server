from fastapi import Depends
from typing import Annotated, Any
from transformers import ZeroShotClassificationPipeline
from supabase import Client

from core.middleware import AuthMiddleware
from core.database import Database
from core.pipeline import Pipeline

GetUser = Annotated[dict[str, Any], Depends(AuthMiddleware.get_user)]
GetDB = Annotated[Client, Depends(Database.get_db)]
GetClassifier = Annotated[ZeroShotClassificationPipeline, Depends(Pipeline.get_classifier)]