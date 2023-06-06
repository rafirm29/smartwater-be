from fastapi import APIRouter, HTTPException, Depends
from repository.user import UserRepository
from models.user import User
from schemas.user import UserData, UserLogin, UserRegister, Token
from db.database import collection

from utils.auth import verify_password, create_access_token

user = APIRouter(prefix='/user', tags=['User'])


@user.get('/all')
async def get_all_user(file_repo: UserRepository = Depends(UserRepository)):
    users = await file_repo.get_all_user()
    return users


@user.get('/', response_model=UserData)
async def get_user_by_name(name: str, file_repo: UserRepository = Depends(UserRepository)):
    user = await file_repo.get_user(name)

    if (user):
        return user
    raise HTTPException(404, f"User '{name}' not found")


@user.post('/register', response_model=UserData)
async def register(data: UserRegister, file_repo: UserRepository = Depends(UserRepository)):
    existing_user = await collection.find_one({'email': data.email})
    if existing_user is not None:
        raise HTTPException(400, 'User already exist')
    response = await file_repo.register(data)
    if response:
        return response
    raise HTTPException(400, 'Something went wrong')


@user.post('/login', response_model=Token)
async def login(data: UserLogin):
    user = await collection.find_one({'email': data.email})
    if user is None:
        raise HTTPException(400, 'No user with the email found')

    hashed_pass = user['password']
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            400, 'Incorrect email or password'
        )

    return {
        'token': create_access_token(data.email)
    }
