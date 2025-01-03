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

from api.misc.custom_logger import DBLogger

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

        if payload.get("role") not in required_role:
            DBLogger.warning(
                message=f"User role was insufficient required role was {required_role} while user role was {payload.get('role')}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Not authorized, required permissions is {required_role}",
            )

        DBLogger.info(message=f"Token was validated for user {payload.get('username')}")
        return payload
    except jwt.ExpiredSignatureError:
        DBLogger.warning(message=f"Expired token {credentials.credentials} was sent")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        DBLogger.warning(message=f"Invalid token {credentials.credentials} was sent")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def validate_user(credentials: HTTPAuthorizationCredentials, db: database.Database):
    user = db["usersdb"].find_one({"username": credentials.username})

    if user is None:
        DBLogger.warning(
            message=f"User {credentials.username} could not validated since was not found in db"
        )
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {credentials.username} not in db",
            headers={"WWW-Authenticate": "Basic"},
        )

    if user and user["password"] == credentials.password:
        DBLogger.info(message=f"User {credentials.username} was successfully validated")
        return user["role"]

    DBLogger.warning(
        message=f"User {credentials.username} could not validated since bad password"
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def get_user_name(
    credentials: HTTPBasicCredentials = Depends(security),
):
    return credentials.username


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
