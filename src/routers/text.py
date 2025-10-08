from fastapi import APIRouter

router = APIRouter(
    prefix="/text"
)

@router.post("/")
async def some_function():
    ...

