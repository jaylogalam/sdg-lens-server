from fastapi import APIRouter

router = APIRouter(
    prefix="/template"
)

@router.get("/")
async def some_function():
    ...

