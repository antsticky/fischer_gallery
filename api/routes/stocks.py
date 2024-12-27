from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer

from dotenv import load_dotenv

from typing import Dict

from api.datamodels.api_inputs import InputAddStockModel
from api.datamodels.api_responses import InsertTypeModel, UniqueValuesHeaderTypeModel
from api.misc.file_handler import FileHandler

from api.middlewares.db_handlers import get_read_write_stockdb
from api.middlewares.jwt_auth import get_jwt_payload_dependency

load_dotenv()

router = APIRouter()
bearer = HTTPBearer()


@router.post("/stock")
async def add_stock(
    input: InputAddStockModel = Depends(),
    stock_img: UploadFile = File(...),
    payload: Dict = Depends(get_jwt_payload_dependency),
) -> InsertTypeModel:
    if "write" not in payload.get("role"):
        raise HTTPException(status_code=401, detail="No write permission")

    FileHandler.validate_file(stock_img)
    file_path = await FileHandler.save_file(stock_img, input.stock_type)

    db = get_read_write_stockdb()
    collection = db["stocks"]

    try:
        result = collection.insert_one(
            {**input.model_dump(), "file_path": str(file_path)}
        )
        return InsertTypeModel(
            message="Entry added successfully", object_id=str(result.inserted_id)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/headers")
async def get_header_names(
    name: str,
    _: Dict = Depends(get_jwt_payload_dependency),
) -> UniqueValuesHeaderTypeModel:

    db = get_read_write_stockdb()
    collection = db["stocks"]

    try:
        return UniqueValuesHeaderTypeModel(
            message=f"Uniques values for column {name}",
            unique_values=collection.distinct(name),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
