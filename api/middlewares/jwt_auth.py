import os
import jwt

from typing import List
from functools import partial

from pymongo import database

from fastapi.security import (
    HTTPBasic,
    HTTPBearer,
    HTTPBasicCredentials,
    HTTPAuthorizationCredentials,
)
from fastapi import HTTPException, status


from fastapi import Depends

from api.middlewares.db_handlers import get_read_userdb


bearer = HTTPBearer()
security = HTTPBasic()

algorithm = "HS256"
secret = os.getenv("JWT_SECRET_KEY")


def validate_jwt_token(
    credentials: HTTPAuthorizationCredentials, required_role: List[str]
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret, algorithms=[algorithm])

        print(payload.get("role"))

        if payload.get("role") not in required_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Not authorized, required permissions is {required_role}",
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def validate_user(credentials: HTTPAuthorizationCredentials, db: database.Database):
    user = db["usersdb"].find_one({"username": credentials.username})

    if user is None:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {credentials.username} not in db",
            headers={"WWW-Authenticate": "Basic"},
        )

    if user and user["password"] == credentials.password:
        return user["role"]

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def get_user_role(
    credentials: HTTPBasicCredentials = Depends(security),
    db: database.Database = Depends(get_read_userdb),
):
    return validate_user(credentials, db)


def get_jwt_payload_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    required_role: List[str] = ["read", "write"],
):
    return validate_jwt_token(credentials=credentials, required_role=required_role)


jwt_read_or_write_dependency = Depends(get_jwt_payload_dependency)
jwt_write_dependency = Depends(
    partial(get_jwt_payload_dependency, required_role=["write"])
)
