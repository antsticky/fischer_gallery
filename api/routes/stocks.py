from typing import Annotated, Dict
from fastapi.security import HTTPBearer
from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Query

from dotenv import load_dotenv


from api.misc.file_handler import FileHandler
from api.datamodels.api_inputs import InputAddStockModel, StockQueryTypeModel
from api.datamodels.api_responses import InsertTypeModel, UniqueValuesHeaderTypeModel

from api.misc.json_converter import flatten_object_id
from api.middlewares.query_builder import get_prepared_query
from api.middlewares.db_handlers import get_read_write_stockdb
from api.middlewares.jwt_auth import get_jwt_payload_dependency


load_dotenv()

router = APIRouter()
bearer = HTTPBearer()


@router.get("/")
async def get_stocks(
    query: StockQueryTypeModel = Depends(get_prepared_query),
    _: Dict = Depends(get_jwt_payload_dependency),
):
    try:
        db = get_read_write_stockdb()
        collection = db["stocks"]

        stocks = [flatten_object_id(doc) for doc in collection.find(query)]
        return {"stocks": stocks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def add_stock(
    input: Annotated[InputAddStockModel, Query()],
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


@router.get("/{column_name}/unique_values")
async def get_unique_names(
    column_name: str,
    query: StockQueryTypeModel = Depends(get_prepared_query),
    _: Dict = Depends(get_jwt_payload_dependency),
) -> UniqueValuesHeaderTypeModel:
    try:
        db = get_read_write_stockdb()
        collection = db["stocks"]
        return UniqueValuesHeaderTypeModel(
            # TODO: mongo splits the value by spaces -– escape it at upload time and modify the search accordingly
            message=f"Uniques values for column {column_name}",
            unique_values=collection.distinct(column_name, query),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))