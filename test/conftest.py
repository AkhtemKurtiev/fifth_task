import asyncio
from typing import AsyncGenerator

from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncConnection,
    create_async_engine
)
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST
from src.database.db import BaseModel, get_async_session
from src.main import app

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
)

async_engine_test = create_async_engine(DATABASE_URL_TEST, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine_test,
    expire_on_commit=False
)

BaseModel.metadata.bind = async_engine_test


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine_test.begin() as conn:
        yield conn


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all())
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all())


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)

@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
