from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from src.api.v1.utils.utils import add_params_in_router_filter
from src.services.spimex import SpimexService
from src.schemas.spimex import Spimex_trading_resultsCreate


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
    service: SpimexService = Depends(SpimexService)
):
    return await service.get_last_trading_dates(count_last_day)


@router.get(
        '/dynamics',
        response_model=List[Spimex_trading_resultsCreate]
)
@cache(expire=120)
async def get_dynamics(
    start_date: date = Query('2024-07-12'),
    end_date: date = Query('2024-07-13'),
    add_params_in_router: tuple = Depends(add_params_in_router_filter),
    service: SpimexService = Depends(SpimexService)
):
    return await service.get_dynamics(
        start_date, end_date, add_params_in_router
    )


@router.get(
        '/trading_results',
        response_model=List[Spimex_trading_resultsCreate]
)
@cache(expire=120)
async def get_trading_results(
    count_last_day: int = 10,
    add_params_in_router: tuple = Depends(add_params_in_router_filter),
    service: SpimexService = Depends(SpimexService)
):
    return await service.get_trading_results(
        count_last_day, add_params_in_router
    )
