from typing import List, Dict
from pydantic import BaseModel

from api.datamodels.token import TokenPayloadTypeModel


class BaseResponseTypeModel(BaseModel):
    message: str


class HealthTypeModel(BaseResponseTypeModel):
    uptime: float


class InsertTypeModel(BaseResponseTypeModel):
    object_id: str


class GetTokenTypeModel(BaseResponseTypeModel):
    token: str


class ValidateTokenTypeModel(BaseResponseTypeModel):
    payload: TokenPayloadTypeModel


class UniqueValuesHeaderTypeModel(BaseResponseTypeModel):
    unique_values: list

    page: int
    per_page: int
    count: int

class GetAllStocksTypeModel(BaseResponseTypeModel):
    stocks: List[Dict]
    
    page: int
    per_page: int
    count: int
