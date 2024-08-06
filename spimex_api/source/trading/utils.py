from typing import Optional, Tuple

from sqlalchemy import Select

from trading.models.spimex_trading_results import Spimex_trading_results


def string_to_date(date: str):
    return int(date[6:10]),  int(date[3:5]), int(date[0:2])


def params_filter(
        query: Select[Tuple[Spimex_trading_results]],
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None
):
    if oil_id:
        query = query.filter(
            Spimex_trading_results.oil_id == oil_id
        )
    if delivery_type_id:
        query = query.filter(
            Spimex_trading_results.delivery_type_id == delivery_type_id
        )
    if delivery_basis_id:
        query = query.filter(
            Spimex_trading_results.delivery_basis_id == delivery_basis_id
        )
    return query


def add_params_in_router_filter(
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
):
    return oil_id, delivery_type_id, delivery_basis_id
