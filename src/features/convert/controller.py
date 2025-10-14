from fastapi import APIRouter

router = APIRouter(
      prefix="/convert"
)

@router.get("/")
def function_name():
    return "Convert route"