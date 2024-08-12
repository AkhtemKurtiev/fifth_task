import pytest


class TestUnitOfWork:
    async def test_commit(self, uow, mock_session):
        async with uow:
            pass
        mock_session.commit.assert_called_once()

    async def test_rollback_on_exception(self, mocker, uow, mock_session):
        mocker.patch(
            'src.utils.unit_of_work.AsyncSessionLocal',
            side_effect=Exception
        )
        with pytest.raises(Exception):
            async with uow:
                raise Exception('Test raise')
        mock_session.rollback.assert_called_once()

    async def test_uow_context_manager(self, uow, mock_session):
        async with uow:
            assert uow.session == mock_session
        mock_session.close.assert_called_once()
