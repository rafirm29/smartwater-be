from db.database import collection
from models.user import User

from utils.auth import get_hashed_password


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

    async def register(self, user: User):
        document = {
            'name': user.name,
            'email': user.email,
            'password': get_hashed_password(user.password)
        }
        await collection.insert_one(document)
        return document
