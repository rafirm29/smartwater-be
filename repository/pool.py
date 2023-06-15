from typing import List

from db.database import collection_pool
from models.pool import Pool
from schemas.user import UserData


class PoolRepository():
    async def get_pool(self, user: UserData):
        pools = await collection_pool.find({"user_email": user['email']}).to_list(1000)
        return pools

    async def get_pool_by_id(self, pool_id: str):
        document = await collection_pool.find_one({'id': pool_id})
        return document

    async def add_pool(self, pool):
        pool_obj = Pool(**pool)
        pool_doc = pool_obj.dict(by_alias=True)

        # Convert _id to id
        pool_doc['id'] = str(pool_doc.pop('_id'))
        await collection_pool.insert_one(pool_doc)

        return pool_doc

    async def add_sensor(self, pool: Pool, sensor: List[str]):
        update_result = await collection_pool.update_one(
            {'id': pool['id']},
            {'$push': {'sensor':  {'$each': sensor}}}
        )

        if update_result:
            return True
        return False
