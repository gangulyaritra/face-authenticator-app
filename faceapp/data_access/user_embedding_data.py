from faceapp.config.database import MongoDBClient
from faceapp.constant import EMBEDDING_COLLECTION_NAME


class UserEmbeddingData:
    def __init__(self) -> None:
        self.client = MongoDBClient()
        self.collection_name = EMBEDDING_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user_embedding(self, uuid_: str, embedding_list) -> None:
        self.collection.insert_one({"UUID": uuid_, "user_embed": embedding_list})

    def get_user_embedding(self, uuid_: str) -> dict:
        user: dict = self.collection.find_one({"UUID": uuid_})
        return user if user != None else None
