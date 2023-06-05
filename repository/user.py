from db.database import collection
from models.user import User


class UserRepository():
    async def get_user(self, name: str):
        document = await collection.find_one({"name": name})
        return document

    async def get_all_user(self):
        users = []
        cursor = collection.find({})
        async for document in cursor:
            users.append(User(**document))
        return users

    async def add_user(self, user):
        document = user
        result = await collection.insert_one(document)
        return document
