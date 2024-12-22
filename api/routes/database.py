from fastapi import APIRouter

router = APIRouter()


@router.get("/endpoint2")
async def endpoint2():
    return {"message": "Endpoint 2"}
