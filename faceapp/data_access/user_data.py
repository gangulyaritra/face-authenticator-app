from faceapp.entity.user import User
from faceapp.config.database import MongoDBClient
from faceapp.constant import USER_COLLECTION_NAME


class UserData:
    def __init__(self) -> None:
        self.client = MongoDBClient()
        self.collection_name = USER_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user(self, user: User) -> None:
        self.collection.insert_one(user)

    def get_user(self, query: dict):
        return self.collection.find_one(query)

    def get_all_users(self):
        pass

    def delete_user(self, user_id: str) -> None:
        pass

    def delete_all_users(self) -> None:
        pass
