from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[T, ID]):

    @abstractmethod
    async def _get_all_items(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def _get_item_by_id(self, item_id: ID) -> T | None:
        raise NotImplementedError

    async def get_all(self) -> list[T]:
        return await self._get_all_items()

    async def get_item_by_id(self, item_id: ID) -> T | None:
        return await self._get_item_by_id(item_id)
