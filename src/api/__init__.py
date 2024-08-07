__all__ = [
    'router'
]

from fastapi import APIRouter

from src.api.v1.routers import v1_spimex_router

router = APIRouter()
router.include_router(v1_spimex_router, prefix='/v1', tags=['v1'])
