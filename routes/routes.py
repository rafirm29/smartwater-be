from fastapi import APIRouter

from routes.user import user
from routes.pool import pool

router = APIRouter()
router.include_router(user)
router.include_router(pool)
