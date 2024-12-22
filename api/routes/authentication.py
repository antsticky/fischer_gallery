from fastapi import APIRouter

router = APIRouter()


@router.get("/endpoint1")
async def endpoint1():
    return {"message": "Endpoint 1"}
