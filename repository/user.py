from db.database import collection_user
from models.user import User

from utils.auth import get_hashed_password


class UserRepository():
    async def get_user(self, name: str):
        document = await collection_user.find_one({"name": name})
        return document

    async def get_all_user(self):
        users = []
        cursor = collection_user.find({})
        async for document in cursor:
            users.append(User(**document))
        return users

    async def register(self, user: User):
        document = {
            'name': user.name,
            'email': user.email,
            'password': get_hashed_password(user.password)
        }
        await collection_user.insert_one(document)
        return document
