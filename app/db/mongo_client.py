from pymongo import MongoClient
from pymongo.errors import OperationFailure

from config import MongoDBConfig as mdb


class MongoDBException(Exception):
    pass


def create_mongo_db_client() -> MongoClient:
    _mongo_url = f"mongodb://localhost:27017/{mdb.db_name}"
    db_client = MongoClient(_mongo_url)
    try:
        # Verify connection is valid
        db_client.server_info()
        print("Database connection succeeded.")
        return db_client
    except OperationFailure:
        raise MongoDBException
    except Exception:
        raise MongoDBException
