from fastapi import APIRouter, HTTPException, Depends
from typing import List

from middleware.auth import get_current_user
from repository.pool import PoolRepository
from schemas.pool import PoolData, AddPool, UpdatePoolName
from schemas.user import UserData


pool = APIRouter(prefix='/pool', tags=['Pool'])


@pool.get('/', response_model=List[PoolData])
async def get_pool(user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    pool = await pool_repo.get_pool(user)

    if pool:
        return pool
    raise HTTPException(404, f"No pools found")


@pool.post('/add', response_model=PoolData)
async def add_pool(pool: AddPool, user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    pool_exist = await pool_repo.get_pool_by_id(pool.id)
    if (pool_exist):
        raise HTTPException(400, f"Pool already exists")

    document = {
        'id': pool.id,
        'user_email': user['email'],
        'name': pool.name
    }
    response = await pool_repo.add_pool(document)
    if response:
        return response
    raise HTTPException(400, f"Failed to add pool")


# @pool.post('/{pool_id}/add-sensor')
# async def add_sensor(pool_id: str, sensor: AddSensor, user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
#     pool = await pool_repo.get_pool_by_id(pool_id)

#     if pool is None:
#         raise HTTPException(404, f"No pool found. Invalid pool id")

#     if pool['user_email'] != user['email']:
#         raise HTTPException(
#             401, f"You are not authenticated to update this pool")

#     response = await pool_repo.add_sensor(pool, sensor.sensor)

#     if response:
#         return {
#             'message': 'Successfully add sensor(s)'
#         }
#     raise HTTPException(status_code=400, detail='Failed to update pool')


@pool.put('/{pool_id}/change-name')
async def change_pool_name(pool_id: str, new_name: UpdatePoolName, user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    pool = await pool_repo.get_pool_by_id(pool_id)

    if pool is None:
        raise HTTPException(404, f"No pool found. Invalid pool id")

    if pool['user_email'] != user['email']:
        raise HTTPException(
            401, f"You are not authenticated to update this pool")

    response = await pool_repo.update_name(pool, new_name.name)

    if response:
        return {
            'message': f"Successfully update pool name to '{new_name.name}'"
        }
    raise HTTPException(status_code=400, detail='Failed to change pool name')


@pool.put('/{pool_id}/set-normal')
async def set_pool_normal(pool_id: str, user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    pool = await pool_repo.get_pool_by_id(pool_id)

    if pool is None:
        raise HTTPException(404, f"No pool found. Invalid pool id")

    if pool['user_email'] != user['email']:
        raise HTTPException(
            403, f"You are not authorized to update this pool")

    response = await pool_repo.set_normal(pool)

    if response:
        return {
            'message': f"Successfully done action to pool"
        }
    raise HTTPException(status_code=400, detail='Failed to do action to pool')


@pool.delete('/{pool_id}/delete')
async def delete_pool(pool_id: str, user: UserData = Depends(get_current_user), pool_repo: PoolRepository = Depends(PoolRepository)):
    pool = await pool_repo.get_pool_by_id(pool_id)

    if pool is None:
        raise HTTPException(404, f"No pool found. Invalid pool id")

    if pool['user_email'] != user['email']:
        raise HTTPException(
            403, f"You are not authorized to delete this pool")

    response = await pool_repo.remove_pool(pool['id'])

    if response:
        return {
            'message': f"Successfully deleted pool"
        }
    raise HTTPException(status_code=400, detail='Failed to do action to pool')
