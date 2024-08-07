from datetime import date

from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.utils.utils import params_filter
from src.models.spimex_trading_results import Spimex_trading_results
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


def params_to_dict(kwargs: dict, add_params_in_router: dict) -> dict:
    if add_params_in_router['oil_id']:
        kwargs['oil_id'] = add_params_in_router['oil_id']
    if add_params_in_router['delivery_type_id']:
        kwargs['delivery_type_id'] = (
            add_params_in_router['delivery_type_id']
        )
    if add_params_in_router['delivery_basis_id']:
        kwargs['delivery_basis_id'] = (
            add_params_in_router['delivery_basis_id']
        )
    return kwargs


class SpimexService(BaseService):
    base_repository: str = 'spimex'

    @transaction_mode
    async def get_last_trading_dates(
        self,
        count_last_day
    ):
        try:
            all_dates = await self.uow.spimex.get_by_query_all()
            distinct_dates = (
                sorted(set(date.date for date in all_dates), reverse=True)
            )
            return distinct_dates[:count_last_day]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
                })

    @transaction_mode
    async def get_dynamics(
        self,
        start_date: date,
        end_date: date,
        add_params_in_router: dict
    ):
        try:
            kwargs = {'date': (start_date, end_date)}
            kwargs = params_to_dict(kwargs, add_params_in_router)
            result = await self.uow.spimex.get_by_query_all(**kwargs)
            return result
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
            })

    @transaction_mode
    async def get_trading_results(
        self,
        count_last_day: int,
        add_params_in_router: dict
    ):
        try:
            kwargs = {}
            kwargs = params_to_dict(kwargs, add_params_in_router)
            results = await self.uow.spimex.get_by_query_all(**kwargs)
            return results[:count_last_day]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'detail': None
            })
