from typing import List, Dict
from pydantic import BaseModel


class BaseResponseTypeModel(BaseModel):
    message: str


class HealthTypeModel(BaseResponseTypeModel):
    uptime: float


class InsertTypeModel(BaseResponseTypeModel):
    object_id: str


class GetTokenTypeModel(BaseResponseTypeModel):
    token: str


class TokenPayloadTypeModel(BaseModel):
    username: str
    role: str
    exp: float


class ValidateTokenTypeModel(BaseResponseTypeModel):
    payload: TokenPayloadTypeModel


class PaginationResponseTypeModel(BaseModel):
    page: int
    per_page: int
    count: int


class UniqueValuesHeaderTypeModel(BaseResponseTypeModel, PaginationResponseTypeModel):
    unique_values: List


class GetAllStocksTypeModel(BaseResponseTypeModel, PaginationResponseTypeModel):
    stocks: List[Dict]
