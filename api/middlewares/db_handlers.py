import os

from pymongo import MongoClient, database

from urllib.parse import quote
from dotenv import load_dotenv


load_dotenv()


mongo_read_userdb_client = MongoClient(
    os.getenv("MONGO_URI_READ"),
    username=os.getenv("MONGO_USER_READ_USERNAME"),
    password=os.getenv(quote("MONGO_USER_READ_PASSWORD")),
    authSource=os.getenv("MONGO_DB_NAME"),
)


def get_read_userdb() -> database.Database:
    return mongo_read_userdb_client[os.getenv("MONGO_DB_NAME")]


mongo_read_write_stockdb_client = MongoClient(
    os.getenv("MONGO_URI_READ"),
    username=os.getenv("MONGO_READ_WRITE_USER"),
    password=os.getenv(quote("MONGO_READ_WRITE_PASSWORD")),
    authSource=os.getenv("MONGO_DB_NAME"),
)


def get_read_write_stockdb() -> database.Database:
    return mongo_read_write_stockdb_client[os.getenv("MONGO_DB_NAME")]


mongo_read_stockdb_client = MongoClient(
    os.getenv("MONGO_URI_READ"),
    username=os.getenv("MONGO_READ_USER"),
    password=os.getenv(quote("MONGO_READ_PASSWORD")),
    authSource=os.getenv("MONGO_DB_NAME"),
)


def get_read_stockdb() -> database.Database:
    return mongo_read_stockdb_client[os.getenv("MONGO_DB_NAME")]
