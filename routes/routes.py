from fastapi import APIRouter

from routes.user import user
from routes.pool import pool
from routes.history import history

router = APIRouter()
router.include_router(user)
router.include_router(pool)
router.include_router(history)
