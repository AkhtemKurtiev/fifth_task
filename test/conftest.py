import asyncio
from typing import AsyncGenerator

from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import pytest
from httpx import AsyncClient
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncConnection,
    create_async_engine
)
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.config import (
    DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST
)
from src.database.db import BaseModel, get_async_session
from src.main import app
from src.utils.repository import SqlAlchemyRepository

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
)

async_engine_test = create_async_engine(DATABASE_URL_TEST, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine_test,
    expire_on_commit=False
)

BaseModel.metadata.bind = async_engine_test


class TestModel(BaseModel):
    __tablename__ = 'test_model'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class TestModelRepository(SqlAlchemyRepository):
    model = TestModel


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine_test.begin() as conn:
        yield conn


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope='session')
async def async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    redis = aioredis.from_url(
        'redis://localhost',
        encoding='utf-8',
        decode_response=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    await redis.close()
