import os
import jwt
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel
from pymongo import MongoClient, database

from fastapi import APIRouter, HTTPException, HTTPException, status
from fastapi.security import (
    HTTPBasic,
    HTTPBearer,
    HTTPBasicCredentials,
    HTTPAuthorizationCredentials,
)


from fastapi import Depends
from dotenv import load_dotenv

router = APIRouter()

security = HTTPBasic()
bearer = HTTPBearer()

load_dotenv()

algorithm = "HS256"
expire_in_seconds = 10 * 60
secret = os.getenv("JWT_SECRET_KEY")

mongo_read_client = MongoClient(
    os.getenv("MONGO_URI_READ"),
    username=os.getenv("MONGO_USER_READ_USERNAME"),
    password=os.getenv("MONGO_USER_READ_PASSWORD"),
    authSource=os.getenv("MONGO_DB_NAME"),
)


def get_read_db() -> database.Database:
    return mongo_read_client[os.getenv("MONGO_DB_NAME")]


class UserTypeModel(BaseModel):
    username: str
    password: str
    role: str


@router.get("/")
def get_jwt_token(
    credentials: HTTPBasicCredentials = Depends(security), db=Depends(get_read_db)
):
    user = db["usersdb"].find_one({"username": credentials.username})

    if user is None:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {credentials.username} not in db",
            headers={"WWW-Authenticate": "Basic"},
        )

    if user and user["password"] == credentials.password:
        payload = {
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expire_in_seconds),
        }

        token = jwt.encode(payload, secret, algorithm)

        return {"token": token}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.get("/validate")
async def validate_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return {"message": "Token is valid", "payload": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
