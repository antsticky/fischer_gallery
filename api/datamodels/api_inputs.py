from fastapi import HTTPException, status

from pydantic import BaseModel
from typing import Optional, Literal, Optional


class InputAddStockModel(BaseModel):
    stock_type: str
    name: str

    artist: str

    year: int
    period_type: Literal["0", "1", "2"]

    style: Optional[str] = None
    price: Optional[float] = None

    @property
    def start_year(self) -> int:
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
