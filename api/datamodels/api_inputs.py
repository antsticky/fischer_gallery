from fastapi import HTTPException, status

from pydantic import BaseModel, field_validator
from typing import Optional, Literal, Optional, List


class InputAddStockModel(BaseModel):
    stock_type: str
    name: str

    artist: str

    period_type: Literal["0", "1", "2"]
    year: List[int] | int

    style: Optional[str] = None
    price: Optional[float] = None

    @field_validator("name", "artist")
    @classmethod
    def string_validator(cls, value: str) -> str:
        if value.startswith("*") or value.endswith("*"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot start or end name or artist field with *",
            )

        return " ".join([word.capitalize() for word in value.split(" ")])

    @field_validator("year")
    @classmethod
    def validate_year(cls, year: List[int] | int, values) -> List[int] | int:
        if isinstance(year, list) and (values.data["period_type"] != "0"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Multiple year value permitted only for period_type = 0",
            )

        if len(year) == 1:
            return year[0]

        if len(year) != 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Year must be either 1 or 2 length",
            )

        if year[0] > year[1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"From year must be smaller then the end year but {year} was given",
            )

    @property
    def start_year(self) -> int:
        if isinstance(self.year, list):
            return self.year[0]

        if self.period_type == "0":
            return self.year

        if len(str(self.year)) != 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"If period_type is 1 or 2 the year must contains 4 digits, but {self.year} was given",
            )

        if self.period_type == "1":
            return (self.year // 10) * 10
        if self.period_type == "2":
            return (self.year // 100) * 100

    @property
    def end_year(self) -> int:
        if isinstance(self.year, list):
            return self.year[1]

        if self.period_type == "0":
            return self.year

        if len(str(self.year)) != 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"If period_type is 1 or 2 the year must contains 4 digits, but {self.year} was given",
            )

        if self.period_type == "1":
            return (self.year // 10) * 10 + 10
        if self.period_type == "2":
            return (self.year // 100) * 100 + 100

    def model_dump(self, *args, **kwargs):
        original_dict = super().model_dump(*args, **kwargs)
        additional_properties = {
            "start_year": self.start_year,
            "end_year": self.end_year,
        }
        return {**original_dict, **additional_properties}


class ExactMatchQueryTypeModel(BaseModel):
    value: str

    def query(self, field_name):
        return {field_name: self.value}


class PatternMatchQueryTypeModel(BaseModel):
    value: str

    def query(self, field_name):
        if "*" not in [self.value[0], self.value[-1]]:
            return {field_name: self.value}
        if self.value[0] == "*" and self.value[-1] == "*":
            return {field_name: {"$regex": f".*{self.value[1:-1]}.*"}}
        if self.value[0] == "*":
            return {field_name: {"$regex": f".*{self.value[1:]}"}}
        if self.value[-1] == "*":
            return {field_name: {"$regex": f"^{self.value[:-1]}.*"}}


class IntervalMatchQueryTypeModel(BaseModel):
    value: list[float] | int

    @property
    def from_value(self):
        return self.value[0] if isinstance(self.value, list) else self.value

    @property
    def to_value(self):
        return self.value[1] if isinstance(self.value, list) else self.value

    def query(self, field_name):
        if self.to_value == -1 and self.from_value == -1:
            return {}
        if self.to_value == -1:
            return {field_name: {"$gte": self.from_value}}
        if self.from_value == -1:
            return {field_name: {"$lte": self.from_value}}

        return {field_name: {"$in": [self.from_value, self.to_value]}}


class StockQueryTypeModel(BaseModel):
    name: Optional[PatternMatchQueryTypeModel] = None
    artist: Optional[PatternMatchQueryTypeModel] = None

    stock_type: Optional[ExactMatchQueryTypeModel] = None
    style: Optional[ExactMatchQueryTypeModel] = None

    year: Optional[IntervalMatchQueryTypeModel] = None
    price: Optional[IntervalMatchQueryTypeModel] = None


class PaginationTypeBaseModel(BaseModel):
    page: int = 1
    per_page: int = 10

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def start_index(self) -> int:
        return self.skip

    @property
    def end_index(self) -> int:
        return self.start_index + self.per_page
