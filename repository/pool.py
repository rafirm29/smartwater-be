from db.database import collection_pool
from models.pool import Pool


class PoolRepository():
    async def get_pool(self, user_id: str):
        pools = []
        cursor = collection_pool.find({"user_email": user_id})
        async for document in cursor:
            pools.append(Pool(**document))
        return pools

    async def add_pool(self, pool: Pool):
        document = pool.dict()
        await collection_pool.insert_one(document)
        return document
