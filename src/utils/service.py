from typing import Any, Optional, Sequence, Union
from uuid import uuid4

from src.utils.unit_of_work import transaction_mode, UnitOfWork


class BaseService:
    base_repository: Optional[str] = None

    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    @transaction_mode
    async def add_one(self, **kwargs: Any) -> None:
        await self.uow.__dict__[self.base_repository].add_one(**kwargs)

    @transaction_mode
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str:
        return await self.uow.__dict__[self.base_repository].add_one_and_get_id(**kwargs)

    @transaction_mode
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        return await self.uow.__dict__[self.base_repository].add_one_and_get_obj(**kwargs)

    @transaction_mode
    async def get_by_query_one_or_none(self, **kwargs: Any) -> Any | None:
        return await self.uow.__dict__[self.base_repository].get_by_query_one_or_none(**kwargs)

    @transaction_mode
    async def get_by_query_all(self, **kwargs: Any) -> Sequence[Any]:
        return await self.uow.__dict__[self.base_repository].get_by_query_all(**kwargs)

    @transaction_mode
    async def update_one_by_id(self, obj_id: Union[int, str, uuid4], values: dict) -> Any:
        return await self.uow.__dict__[self.base_repository].get_by_query_all(obj_id=obj_id, values=values)

    @transaction_mode
    async def delete_by_query(self, **kwargs: Any) -> None:
        return await self.uow.__dict__[self.base_repository].delete_by_query(**kwargs)

    @transaction_mode
    async def delete_all(self) -> None:
        return await self.uow.__dict__[self.base_repository].delete_all()
