from mongo_client import create_mongo_db_client

from config import MongoDBConfig as mdb


class MongoDBUtils:
    def __init__(self):
        self.collection = create_mongo_db_client()[mdb.db_name][mdb.collection_name]

    def db_insert_test(self, document: dict):
        if document:
            resp = self.collection.insert_one(document)
            return resp.inserted_ids
        return None

    def db_find_test(self, filter_query: dict, projection: dict) -> list:
        documents = self.collection.find(filter_query, projection=projection)
        return list(documents)

    def db_delete_test(self, filter_query: dict):
        resp = self.collection.delete_many(filter_query)
        return resp.deleted_count
