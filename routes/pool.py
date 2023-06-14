from fastapi import APIRouter, HTTPException, Depends
from typing import List

from middleware.auth import get_current_user
from repository.pool import PoolRepository
from schemas.pool import PoolData, AddPool
from schemas.user import UserData


pool = APIRouter(prefix='/pool', tags=['Pool'])


@pool.get('/', response_model=List[PoolData])
async def get_pool(user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    pool = await pool_repo.get_pool(user.email)

    if pool:
        return pool
    raise HTTPException(404, f"No pools found")


@pool.post('/add', response_model=PoolData)
async def add_pool(pool: AddPool, user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    document = {
        'user_email': user.email,
        'name': pool.name,
        'sensor': pool.sensor
    }
    response = await pool_repo.add_pool(document)
    if response:
        return response
    raise HTTPException(404, f"No pools found")
