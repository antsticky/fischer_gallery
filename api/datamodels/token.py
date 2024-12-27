from pydantic import BaseModel


class TokenPayloadTypeModel(BaseModel):
    role: str
    exp: float
