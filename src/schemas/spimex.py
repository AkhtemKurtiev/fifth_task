from datetime import datetime, date

from pydantic import BaseModel


class Spimex_trading_resultsCreate(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: date
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
