from pydantic import BaseModel


class HealthTypeModel(BaseModel):
    message: str
    uptime: float
