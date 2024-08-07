from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.api.v1.routers import v1_spimex_router


async def startup():
    redis = aioredis.from_url(
        'redis://localhost',
        encoding='utf-8',
        decode_response=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    return redis


async def clear_cache():
    await app.state.redis.flushdb()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await startup()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_cache, CronTrigger(hour=14, minute=11))
    scheduler.start()
    yield
    await app.state.redis.close()


app = FastAPI(
    title='SpimexAPI',
    lifespan=lifespan
)

app.include_router(v1_spimex_router)
