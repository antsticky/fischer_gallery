import os
from pathlib import Path
from datetime import datetime


from fastapi import UploadFile, HTTPException


ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/gif"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
FILE_ROOT_FOLDER = Path(os.getenv("FILE_ROOT_FOLDER"))


class FileHandler:
    @staticmethod
    async def save_file(file: UploadFile, stock_type: str):
        try:
            contents = await file.read()

            file_sub_path = Path(stock_type)
            file_path = (
                FILE_ROOT_FOLDER
                / file_sub_path
                / f"{file.filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(
                file_path,
                "wb",
            ) as f:
                f.write(contents)

            return file_sub_path / file.filename
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def validate_file(file: UploadFile):
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type"
            )

        if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file extension"
            )
