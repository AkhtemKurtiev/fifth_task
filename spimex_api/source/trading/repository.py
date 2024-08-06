from datetime import date

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from trading.models.spimex_trading_results import Spimex_trading_results
from .utils import params_filter


class SpimexRepository:

    @staticmethod
    async def get_last_trading_dates(
        count_last_day,
        session: AsyncSession
    ):

        query = select(Spimex_trading_results.date).distinct().order_by(
            desc(Spimex_trading_results.date)).limit(count_last_day)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_dynamics(
        start_date: date,
        end_date: date,
        add_params_in_router: tuple,
        session: AsyncSession
    ):

        query = select(Spimex_trading_results).filter(
            Spimex_trading_results.date.between(start_date, end_date)
            ).order_by(
            desc(Spimex_trading_results.date))
        query = params_filter(query, *add_params_in_router)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_trading_results(
        count_last_day: int,
        add_params_in_router: tuple,
        session: AsyncSession
    ):
        query = select(Spimex_trading_results).order_by(
            desc(Spimex_trading_results.date)).limit(count_last_day)
        query = params_filter(query, *add_params_in_router)
        result = await session.execute(query)
        return result.scalars().all()
