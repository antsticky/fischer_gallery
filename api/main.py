import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from time import time


from api.datamodels.api_responses import HealthTypeModel

from api.misc.date_converter import human_readable_timedelta

from api.routes.authentication import router as auth_router
from api.routes.stocks import router as stocks_router


t0 = time()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Probe"])
async def health() -> HealthTypeModel:
    t1 = time()
    return HealthTypeModel(
        message=f"Up-and-running in the last {human_readable_timedelta(t1-t0)}",
        uptime=round(t1 - t0, 2),
    )


app.include_router(auth_router, prefix="/api/jwt", tags=["Authentication"])
app.include_router(stocks_router, prefix="/api/stocks", tags=["Stocks"])


def run():
    uvicorn.run("api.main:app", host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    run()
