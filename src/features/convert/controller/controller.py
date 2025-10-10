from fastapi import APIRouter

router = APIRouter(
      prefix="/convert"
)

@router.get("/text")
def convert_text():
    ...