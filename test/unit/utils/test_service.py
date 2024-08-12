from datetime import date

from src.models.spimex_trading_results import Spimex_trading_results
from src.services.spimex import params_to_dict


class TestSpimexService:
    async def test_get_last_trading_dates(
            self, mocker, spimex_service, mock_uow
    ):
        count_last_day = 2
        mock_uow.spimex.get_by_query_all.return_value = [
            Spimex_trading_results(date=date(2024, 8, 1)),
            Spimex_trading_results(date=date(2024, 8, 2)),
            Spimex_trading_results(date=date(2024, 8, 3)),
        ]

        result = await spimex_service.get_last_trading_dates(count_last_day)
        assert result == [date(2024, 8, 3), date(2024, 8, 2)]

    async def test_get_dynamics(self, spimex_service, mock_uow):
        start_date = date(2024, 6, 1)
        end_date = date(2024, 6, 15)
        mock_uow.spimex.get_by_query_all.return_value = [
            Spimex_trading_results(date=date(2024, 6, 8), oil_id='A592'),
            Spimex_trading_results(date=date(2024, 6, 9), oil_id='A592'),
        ]

        result = await spimex_service.get_dynamics(
            start_date,
            end_date,
            {
                'oil_id': 'A592',
                'delivery_type_id': None,
                'delivery_basis_id': None
            }
        )
        assert len(result) == 2
        assert result[0].oil_id == 'A592'
        assert result[1].oil_id == 'A592'

    async def test_get_trading_results(self, spimex_service, mock_uow):
        count_last_day = 3
        mock_uow.spimex.get_by_query_all.return_value = [
            Spimex_trading_results(date=date(2024, 6, 8), oil_id='A592'),
            Spimex_trading_results(date=date(2024, 6, 9), oil_id='A592'),
            Spimex_trading_results(date=date(2024, 6, 9), oil_id='A592'),
            Spimex_trading_results(date=date(2024, 6, 10), oil_id='A592'),
        ]
        result = await spimex_service.get_trading_results(
            count_last_day,
            {
                'oil_id': None,
                'delivery_type_id': None,
                'delivery_basis_id': None
            }
        )
        assert len(result) == 3


class TestHelpFunctionService:
    async def test_params_to_dict(self):
        kwargs = {'date': ('2024-07-12', '2024-07-13')}
        add_params_in_router = {
            'oil_id': 'A10K',
            'delivery_type_id': None,
            'delivery_basis_id': None
        }
        result = params_to_dict(kwargs, add_params_in_router)
        assert 'oil_id' in result
        assert result == {
            'date': ('2024-07-12', '2024-07-13'),
            'oil_id': 'A10K',
        }
