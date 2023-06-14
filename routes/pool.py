from fastapi import APIRouter, HTTPException, Depends
from repository.pool import PoolRepository
from schemas.pool import PoolData, AddPool

from typing import List

pool = APIRouter(prefix='/pool', tags=['Pool'])


@pool.get('/', response_model=List[PoolData])
async def get_pool(user_id: str, pool_repo: PoolRepository = Depends(PoolRepository)):
    pool = await pool_repo.get_pool(user_id)

    if pool:
        return pool
    raise HTTPException(404, f"No pools found")


@pool.post('/add', response_model=PoolData)
async def add_pool(pool: AddPool, pool_repo: PoolRepository = Depends(PoolRepository)):
    response = await pool_repo.add_pool(pool)
    if response:
        return response
    raise HTTPException(404, f"No pools found")
