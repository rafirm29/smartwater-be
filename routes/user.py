from fastapi import APIRouter, HTTPException, Depends
from repository.user import UserRepository
from models.user import User

user = APIRouter(prefix='/user', tags=['User'])


@user.get('/all')
async def get_all_user(file_repo: UserRepository = Depends(UserRepository)):
    users = await file_repo.get_all_user()
    return users


@user.get('/', response_model=User)
async def get_user_by_name(name: str, file_repo: UserRepository = Depends(UserRepository)):
    user = await file_repo.get_user(name)

    if (user):
        return user
    raise HTTPException(404, f"User '{name}' not found")


@user.post('/add', response_model=User)
async def add_user(user: User, file_repo: UserRepository = Depends(UserRepository)):
    response = await file_repo.add_user(user.dict())
    if response:
        return response
    raise HTTPException(400, 'Something went wrong')
