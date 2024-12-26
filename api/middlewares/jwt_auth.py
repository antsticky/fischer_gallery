import os
import jwt

from pymongo import database
from fastapi import HTTPException, HTTPException, status
from fastapi.security import (
    HTTPBasic,
    HTTPBearer,
    HTTPBasicCredentials,
    HTTPAuthorizationCredentials,
)

from fastapi import Depends


from api.middlewares.db_handlers import get_read_userdb


security = HTTPBasic()
bearer = HTTPBearer()

algorithm = "HS256"
secret = os.getenv("JWT_SECRET_KEY")


def validate_jwt_token(credentials: HTTPAuthorizationCredentials):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret, algorithms=[algorithm])
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
):
    return validate_jwt_token(credentials)
