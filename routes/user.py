from fastapi import APIRouter, HTTPException, Depends
from typing import List

from repository.user import UserRepository
from schemas.user import UserData, UserLogin, UserRegister, LoginResponse, UserChangeName
from db.database import collection_user
from utils.auth import verify_password, create_access_token
from middleware.auth import get_current_user

user = APIRouter(prefix='/user', tags=['User'])


@user.get('/all', response_model=List[UserData])
async def get_all_user(user_repo: UserRepository = Depends(UserRepository)):
    users = await user_repo.get_all_user()
    return users


@user.get('/me', response_model=UserData)
async def get_current_user(user: UserData = Depends(get_current_user)):
    if (user):
        return user
    raise HTTPException(404, f"User not found")


@user.post('/register', response_model=UserData)
async def register(data: UserRegister, user_repo: UserRepository = Depends(UserRepository)):
    existing_user = await collection_user.find_one({'email': data.email})
    if existing_user is not None:
        raise HTTPException(400, 'User already exist')
    response = await user_repo.register(data)
    if response:
        return response
    raise HTTPException(400, 'Something went wrong')


@user.post('/login', response_model=LoginResponse)
async def login(data: UserLogin):
    user = await collection_user.find_one({'email': data.email})
    if user is None:
        raise HTTPException(400, 'No user with the email found')

    hashed_pass = user['password']
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            400, 'Incorrect email or password'
        )

    update_device = await collection_user.update_one(
        {'email': user['email']},
        {"$set": {"device_id": data.device_id}}
    )

    if (not update_device):
        print('Failed to update user device id')

    return {
        'token': create_access_token(data.email),
        'name': user['name'],
        'email': user['email']
    }


@user.put('/change-name', response_model=UserData)
async def change_name(payload: UserChangeName, user: UserData = Depends(get_current_user), user_repo: UserRepository = Depends(UserRepository)):
    response = await user_repo.change_name(user['email'], payload.name)

    if response:
        user['name'] = payload.name
        return user
    raise HTTPException(status_code=400, detail='Failed to do action to pool')
