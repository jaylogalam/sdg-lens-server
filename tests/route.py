from fastapi import APIRouter, Request, Response
from db.supabase import read_item

router = APIRouter(
    prefix="/test"
)

@router.get("/")
def test():
    request: Request
    data = None

    data = read_item()
    
    if data is None:
        return Response("No data")

    return data

