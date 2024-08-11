import pytest
from unittest.mock import AsyncMock, MagicMock

from src.utils.unit_of_work import UnitOfWork, transaction_mode


@pytest.fixture
def mock_session(mocker):
    session = mocker.MagicMock()
    session.commit = mocker.AsyncMock()
    session.rollback = mocker.AsyncMock()
    session.close = mocker.AsyncMock()
    return session


@pytest.fixture
def mock_session_factory(mocker, mock_session):
    factory = mocker.MagicMock(return_value=mock_session)
    return factory


@pytest.fixture
def mock_spimex_repository(mocker, mock_session):
    return mocker.MagicMock()


@pytest.fixture
def uow(mocker, mock_session_factory, mock_spimex_repository):
    mocker.patch(
        'src.utils.unit_of_work.AsyncSessionLocal',
        mock_session_factory
    )
    uow = UnitOfWork()
    uow.spimex = mock_spimex_repository
    return uow
