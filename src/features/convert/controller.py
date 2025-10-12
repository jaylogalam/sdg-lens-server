from fastapi import APIRouter

router = APIRouter(
      prefix="/example"
)

@router.get("/")
def function_name():
    ...