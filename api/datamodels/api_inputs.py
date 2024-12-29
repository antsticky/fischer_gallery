from fastapi import HTTPException, status

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, Literal, Optional, List


class InputAddStockModel(BaseModel):
    stock_type: str
    name: str

    artist: str

    period_type: Literal["0", "1", "2"]
    year: List[int] | int

    style: Optional[str] = None
    price: Optional[float] = None

    @field_validator("year")
    @classmethod
    def validate_year(cls, year: List[int] | int, values) -> List[int] | int:
        if isinstance(year, list) and (values.data["period_type"] != "0"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Multiple year value permitted only for period_type = 0",
            )

        if len(year) == 1:
            return year[0]
        elif len(year) == 2:
            return year

        raise ValueError("Year must be either 1 or 2 length")

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
