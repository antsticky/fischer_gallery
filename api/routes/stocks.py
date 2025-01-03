from typing import Annotated
from pymongo.collection import Collection

from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, UploadFile, HTTPException, Request, Depends, File, Query

from dotenv import load_dotenv


from api.misc.file_handler import FileHandler
from api.datamodels.api_responses import (
    InsertTypeModel,
    UniqueValuesHeaderTypeModel,
    GetAllStocksTypeModel,
)
from api.datamodels.api_inputs import (
    InputAddStockModel,
    StockQueryTypeModel,
    PaginationTypeBaseModel,
)

from api.misc.json_converter import flatten_object_id
from api.middlewares.query_builder import get_prepared_query, get_pagination
from api.middlewares.db_handlers import get_read_write_stockdb, get_read_stockdb

from api.middlewares.jwt_auth import jwt_read_or_write_dependency, jwt_write_dependency

load_dotenv()

router = APIRouter()
bearer = HTTPBearer()


@router.get("/", dependencies=[jwt_read_or_write_dependency])
async def get_stocks(
    query: StockQueryTypeModel = Depends(get_prepared_query),
    pagination: PaginationTypeBaseModel = Depends(get_pagination),
    stocks_read_collection: Collection = Depends(lambda: get_read_stockdb()["stocks"]),
) -> GetAllStocksTypeModel:
    try:
        total_count = stocks_read_collection.count_documents(query)

        stocks = [
            flatten_object_id(doc)
            for doc in stocks_read_collection.find(query)
            .skip(pagination.skip)
            .limit(pagination.per_page)
        ]

        return GetAllStocksTypeModel(
            message=f"Stocks for query: {query}",
            stocks=stocks,
            count=total_count,
            page=pagination.page,
            per_page=pagination.per_page,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", dependencies=[jwt_write_dependency])
async def add_stock(
    input: Annotated[InputAddStockModel, Query()],
    stock_img: UploadFile = File(...),
    stocks_read_write_collection: Collection = Depends(
        lambda: get_read_write_stockdb()["stocks"]
    ),
) -> InsertTypeModel:
    FileHandler.validate_file(stock_img)
    file_path = await FileHandler.save_file(stock_img, input.stock_type)

    try:
        result = stocks_read_write_collection.insert_one(
            {**input.model_dump(), "file_path": str(file_path)}
        )
        return InsertTypeModel(
            message="Entry added successfully", object_id=str(result.inserted_id)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{column_name}/unique_values", dependencies=[jwt_read_or_write_dependency])
async def get_unique_names(
    column_name: str,
    query: StockQueryTypeModel = Depends(get_prepared_query),
    pagination: PaginationTypeBaseModel = Depends(get_pagination),
    stocks_read_collection: Collection = Depends(lambda: get_read_stockdb()["stocks"]),
) -> UniqueValuesHeaderTypeModel:
    try:
        unique_values = stocks_read_collection.distinct(column_name, query)

        return UniqueValuesHeaderTypeModel(
            # TODO: mongo splits the value by spaces -– escape it at upload time and modify the search accordingly
            # pipeline = [ {"$match": query},
            # {"$group": {"_id": None, "distinct_values": {"$addToSet": "$name"}}}
            # ]
            message=f"Uniques values for column {column_name}",
            unique_values=unique_values[pagination.start_index : pagination.end_index],
            page=pagination.page,
            per_page=pagination.per_page,
            count=len(unique_values),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/api/stocks/files/{file_path:path}", dependencies=[jwt_read_or_write_dependency]
)
async def serve_static_files(request: Request, file_path: str):
    return await StaticFiles(directory="files").get_response(
        file_path, scope=request.scope
    )
