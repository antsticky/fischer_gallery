from time import time
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.authentication import router as auth_router
from api.routes.database import router as db_two

from api.datamodels.api_responses import HealthTypeModel

from api.misc.date_converter import human_readable_timedelta

t0 = time()

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
async def home():
    t1 = time()
    return HealthTypeModel(
        message=f"Up-and-running in the last {human_readable_timedelta(t1-t0)}",
        uptime=t1 - t0,
    )


app.include_router(auth_router, prefix="/api/jwt")
app.include_router(db_two, prefix="/api")


def run():
    uvicorn.run("api.main:app", host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    run()
