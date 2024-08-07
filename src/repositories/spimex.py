from src.models.spimex_trading_results import Spimex_trading_results
from src.utils.repository import SqlAlchemyRepository


class SpimexRepository(SqlAlchemyRepository):
    model = Spimex_trading_results
