import pytest

from src.services.spimex import SpimexService
from src.utils.unit_of_work import UnitOfWork
from test.conftest import AsyncSession, TestModelRepository


@pytest.fixture
async def repository(async_session: AsyncSession) -> TestModelRepository:
    return TestModelRepository(session=async_session)


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


@pytest.fixture
def mock_uow(mocker):
    mock_uow = mocker.MagicMock()
    mock_uow.spimex.get_by_query_all = mocker.AsyncMock()
    return mock_uow


@pytest.yield_fixture
def spimex_service(mock_uow):
    service = SpimexService()
    service.uow = mock_uow
    return service
