from db.database import collection_user
from models.user import User
from schemas.user import UserRegister

from services.auth import get_hashed_password


class UserRepository():
    async def get_user(self, email: str):
        document = await collection_user.find_one({"email": email})
        return document

    async def get_all_user(self):
        users = await collection_user.find().to_list(1000)
        return users

    async def register(self, user: UserRegister):
        document = {
            'name': user.name,
            'email': user.email,
            'password': get_hashed_password(user.password)
        }

        user_obj = User(**document)
        user_doc = user_obj.dict(by_alias=True)

        # Convert _id to id
        user_doc['id'] = str(user_doc.pop('_id'))

        await collection_user.insert_one(user_doc)
        return user_doc

    async def change_name(self, email: str, new_name: str):
        update_result = await collection_user.update_one(
            {'email': email},
            {"$set": {"name": new_name}}
        )

        if update_result:
            return True
        return False
