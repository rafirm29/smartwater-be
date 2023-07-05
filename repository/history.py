from db.database import collection_history
from repository.pool import PoolRepository
from models.history import History, DataPoint

import datetime


class HistoryRepository():
    async def get_all_history(self):
        histories = await collection_history.find().to_list(10000)
        return histories

    async def get_history_by_pool(self, pool_id: str):
        history = await collection_history.find_one({'pool_id': pool_id})
        return history

    async def add_record(self, pool_id: str, data: DataPoint):
        # Check if pool_id is valid
        pool_repo = PoolRepository()
        pool = await pool_repo.get_pool_by_id(pool_id=pool_id)

        if pool is None:
            return False

        # Add history record
        existing_history = await collection_history.find_one({"pool_id": pool_id})
        if existing_history:
            history = History(**existing_history)
            history.data.append(data)
            await collection_history.update_one(
                {"pool_id": pool_id}, {"$set": history.dict()})
            return history
        else:
            history = History(pool_id=pool_id, data=[data])
            await collection_history.insert_one(history.dict())
            return history

    async def get_15_latest_data(self, pool_id):
        history = await collection_history.find_one({'pool_id': pool_id})
        if history:
            data = history['data']
            return data[-15:]
        return []
