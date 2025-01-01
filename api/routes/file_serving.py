from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.middlewares.jwt_auth import validate_jwt_token

bearer = HTTPBearer()


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(
                        status_code=401, detail="Invalid authentication scheme"
                    )

                credentials = HTTPAuthorizationCredentials(
                    scheme="bearer", credentials=token
                )

                jwt_payload = validate_jwt_token(credentials)
                request.state.jwt_payload = jwt_payload
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": str(e)})
        else:
            return JSONResponse(
                status_code=401, content={"detail": "Authorization header missing"}
            )

        response = await call_next(request)
        return response


router = FastAPI()
router.add_middleware(JWTAuthMiddleware)
router.mount("/", StaticFiles(directory="files"), name="static")
