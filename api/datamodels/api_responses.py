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


class PaginationResponseTypeModel(BaseModel):
    page: int
    per_page: int
    count: int


class UniqueValuesHeaderTypeModel(BaseResponseTypeModel, PaginationResponseTypeModel):
    unique_values: list


class GetAllStocksTypeModel(BaseResponseTypeModel, PaginationResponseTypeModel):
    stocks: List[Dict]
