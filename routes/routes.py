from fastapi import APIRouter

from routes.user import user
from routes.pool import pool
from routes.history import history
from routes.antares import antares

router = APIRouter()
router.include_router(antares)
router.include_router(user)
router.include_router(pool)
router.include_router(history)
