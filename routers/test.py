from fastapi import APIRouter

router = APIRouter(
    prefix="/test"
)

@router.get("")
async def test():
    data: any
    
    return data or "No data"

