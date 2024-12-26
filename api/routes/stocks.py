from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer


from dotenv import load_dotenv


from api.datamodels.api_inputs import InputAddStockModel
from api.middlewares.db_handlers import get_read_stockdb

load_dotenv()

router = APIRouter()
bearer = HTTPBearer()


@router.post("/stock")
async def add_stock(
    input: InputAddStockModel = Depends(),
    stock_img: UploadFile = File(...),
):
    FileHandler.validate_file(stock_img)
    file_path = await FileHandler.save_file(stock_img, input.stock_type)

    db = get_read_stockdb()
    collection = db["stocks"]

    try:
        result = collection.insert_one(
            {**input.model_dump(), "file_path": str(file_path)}
        )
        return {
            "message": "Entry added successfully",
            "entry_id": str(result.inserted_id),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
