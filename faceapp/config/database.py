import certifi
import pymongo
from faceapp.constant import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        if MongoDBClient.client is None:
            mongo_db_url = MONGODB_URL_KEY
            if "localhost" in mongo_db_url:
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            else:
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

        self.client = MongoDBClient.client
        self.database = self.client[database_name]
        self.database_name = database_name
