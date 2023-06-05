from fastapi import APIRouter

from routes.user import user

router = APIRouter()
router.include_router(user)
