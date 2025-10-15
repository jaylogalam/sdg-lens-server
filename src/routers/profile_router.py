from fastapi import APIRouter

router = APIRouter(
    prefix="/profile"
)

@router.get("/")
def get_profile():
    ...