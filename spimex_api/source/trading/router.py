from datetime import date
import time
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from trading.models.spimex_trading_results import Spimex_trading_results
from .schemas import Spimex_trading_resultsCreate
from .utils import add_params_in_router, params_filter

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
        query = select(Spimex_trading_results.date).distinct().order_by(
            desc(Spimex_trading_results.date)).limit(count_last_day)
        result = await session.execute(query)
        return result.scalars().all()
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
    add_params_in_router: tuple = Depends(add_params_in_router),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Spimex_trading_results).filter(
            Spimex_trading_results.date.between(start_date, end_date)
            ).order_by(
            desc(Spimex_trading_results.date))
        query = params_filter(query, *add_params_in_router)
        result = await session.execute(query)
        return result.scalars().all()
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
    add_params_in_router: tuple = Depends(add_params_in_router),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Spimex_trading_results).order_by(
            desc(Spimex_trading_results.date)).limit(count_last_day)
        query = params_filter(query, *add_params_in_router)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'detail': None
        })
