from fastapi import APIRouter, HTTPException, Depends
from typing import List

from middleware.auth import get_current_user
from repository.history import HistoryRepository
from models.history import DataPoint
from schemas.history import HistoryData, SensorData
from schemas.user import UserData


history = APIRouter(prefix='/history', tags=['History'])


@history.get('/all', response_model=List[HistoryData])
async def get_all_history(history_repo: HistoryRepository = Depends(HistoryRepository)):
    histories = await history_repo.get_all_history()

    if histories:
        return histories
    raise HTTPException(404, f"No history found")


@history.get('/{pool_id}', response_model=HistoryData)
async def get_history_by_pool(pool_id: str, history_repo: HistoryRepository = Depends(HistoryRepository)):
    history = await history_repo.get_history_by_pool(pool_id)

    if history:
        return history
    raise HTTPException(404, f"No history found")


@history.post('/{pool_id}', response_model=HistoryData)
async def add_record(pool_id: str, record: SensorData, history_repo: HistoryRepository = Depends(HistoryRepository)):
    data = record.dict()
    new_record = DataPoint(**data)

    response = await history_repo.add_record(pool_id, new_record)

    if not response:
        raise HTTPException(400, f"Invalid pool id")

    return response
