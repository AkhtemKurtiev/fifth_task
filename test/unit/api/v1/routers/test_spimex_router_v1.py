from httpx import AsyncClient

from src.api.v1.utils.utils import add_params_in_router_filter


class TestEndPoints:
    async def test_get_last_trading_dates(self, ac: AsyncClient):
        response = await ac.get(
            '/trading_result/last_trading_dates?count_last_day=10'
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 10
        for trading_date in data:
            assert isinstance(trading_date, str)

    async def test_get_dynamics(self, ac: AsyncClient):
        response = await ac.get(
            '/trading_result/dynamics?start_date=2024-07-12&end_date=2024-07-13&oil_id=A10K'
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for result in data:
            assert result['oil_id'] == 'A10K'

    async def test_get_trading_result(self, ac: AsyncClient):
        response = await ac.get(
            '/trading_result/trading_results?count_last_day=10&oil_id=A10K'
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 10
        for result in data:
            assert result['oil_id'] == 'A10K'


class TestHelpFunctionEndPoint:
    async def test_add_params_in_router_filter(self):
        result = add_params_in_router_filter('A592')
        assert result == {
            'oil_id': 'A592',
            'delivery_type_id': None,
            'delivery_basis_id': None
        }
