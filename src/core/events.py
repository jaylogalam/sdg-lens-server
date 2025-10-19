from fastapi import FastAPI
from core.pipeline import Pipeline

class Startup:
    @staticmethod        
    def register(app: FastAPI):
        app.add_event_handler("startup", Pipeline.load_classifier_model) # type: ignore