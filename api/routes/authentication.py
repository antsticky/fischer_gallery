import os
import jwt
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from fastapi.security import (
    HTTPBasic,
    HTTPBearer,
)

from fastapi import Depends
from dotenv import load_dotenv

from typing import Dict

from api.datamodels.api_responses import GetTokenTypeModel, ValidateTokenTypeModel
from api.middlewares.jwt_auth import get_user_role, get_jwt_payload_dependency


router = APIRouter()

security = HTTPBasic()
bearer = HTTPBearer()

load_dotenv()

algorithm = "HS256"
expire_in_seconds = 10 * 60
secret = os.getenv("JWT_SECRET_KEY")


@router.get("/")
def get_jwt_token(user_role: str = Depends(get_user_role)) -> GetTokenTypeModel:
    payload = {
        "role": user_role,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expire_in_seconds),
    }
    token = jwt.encode(payload, secret, algorithm)

    return GetTokenTypeModel(
        message="Token is issued",
        token=token,
    )


@router.get("/validate")
async def get_jwt_payload(
    payload: Dict = Depends(get_jwt_payload_dependency),
) -> ValidateTokenTypeModel:
    return ValidateTokenTypeModel(message="Token is valid", payload=payload)
