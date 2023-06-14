from fastapi import APIRouter, HTTPException, Depends
from typing import List

from repository.user import UserRepository
from schemas.user import UserData, UserLogin, UserRegister, LoginResponse
from db.database import collection_user
from utils.auth import verify_password, create_access_token
from middleware.auth import get_current_user

user = APIRouter(prefix='/user', tags=['User'])


# @user.get('/all', response_model=List[UserData])
# async def get_all_user(file_repo: UserRepository = Depends(UserRepository)):
#     users = await file_repo.get_all_user()
#     return users


@user.get('/me', response_model=UserData)
async def get_current_user(user: UserData = Depends(get_current_user)):
    if (user):
        return user
    raise HTTPException(404, f"User not found")


@user.post('/register', response_model=UserData)
async def register(data: UserRegister, file_repo: UserRepository = Depends(UserRepository)):
    existing_user = await collection_user.find_one({'email': data.email})
    if existing_user is not None:
        raise HTTPException(400, 'User already exist')
    response = await file_repo.register(data)
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

    return {
        'token': create_access_token(data.email),
        'name': user['name'],
        'email': user['email']
    }
