from datetime import datetime

from pymongo.collection import Collection


from api.middlewares.db_handlers import get_read_write_stockdb


class DBLogger:
    @staticmethod
    def info(message: str, collection: Collection = None):
        DBLogger.__logging(level="info", message=message, collection=collection)

    @staticmethod
    def error(message: str, collection: Collection = None):
        DBLogger.__logging(level="error", message=message, collection=collection)

    @staticmethod
    def warning(message: str, collection: Collection = None):
        DBLogger.__logging(level="warning", message=message, collection=collection)

    @staticmethod
    def __logging(level: str, message: str, collection: Collection = None):
        collection = (
            get_read_write_stockdb()["logs"] if collection is None else collection
        )
        try:
            collection.insert_one(
                {
                    "level": level,
                    "message": message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        except Exception as e:
            print(f"Failed to log: {message}. Error: {str(e)}")
