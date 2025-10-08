from fastapi import APIRouter, Request, Response

router = APIRouter(
    prefix="/test"
)

@router.get("/")
def test():
    request: Request
    data = None
    
    if data is None:
        return Response("No data")

    return Response(data)

