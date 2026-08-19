from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    status_code: int = 200
    data: Optional[T] = None


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationMeta
