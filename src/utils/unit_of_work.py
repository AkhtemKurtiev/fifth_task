from abc import ABC, abstractmethod
import functools
from types import TracebackType
from typing import Any

from src.database.db import AsyncSessionLocal
from src.repositories.spimex import SpimexRepository


class AbstractUnitOfWork(ABC):
    spimex: SpimexRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.session_factory = AsyncSessionLocal

    async def __aenter__(self):
        self.session = self.session_factory()
        self.spimex = SpimexRepository(self.session)

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def transaction_mode(func):

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
