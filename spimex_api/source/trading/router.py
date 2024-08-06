from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .repository import SpimexRepository
from .schemas import Spimex_trading_resultsCreate
from .utils import add_params_in_router_filter

router = APIRouter(
    prefix='/trading_result',
    tags=['Trading result']
)


@router.get(
        '/last_trading_dates',
        response_model=List[date]
)
@cache(expire=120)
async def get_last_trading_dates(
    count_last_day: int = 10,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await SpimexRepository.get_last_trading_dates(
            count_last_day,
            session
        )
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': None
        })


@router.get(
        '/dynamics',
        response_model=List[Spimex_trading_resultsCreate]
)
@cache(expire=120)
async def get_dynamics(
    start_date: date = Query('2024-07-12'),
    end_date: date = Query('2024-07-13'),
    add_params_in_router: tuple = Depends(add_params_in_router_filter),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await SpimexRepository.get_dynamics(
            start_date,
            end_date,
            add_params_in_router,
            session
        )
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': None
        })


@router.get(
        '/trading_results',
        response_model=List[Spimex_trading_resultsCreate]
)
@cache(expire=120)
async def get_trading_results(
    count_last_day: int = 10,
    add_params_in_router: tuple = Depends(add_params_in_router_filter),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await SpimexRepository.get_trading_results(
            count_last_day,
            add_params_in_router,
            session
        )
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': None
        })


# def func():
#     a = 1
#     yield a
#     b = 2
#     yield b
#     print("Stop")


# @router.get("/")
# async def hello(data=Depends(func)):
#     return {"data": data}
