"""HTTP JSON responses compatible with ``json.dumps`` without per-model ``model_dump(mode=\"json\")``.

Dùng :func:`fastapi.encoders.jsonable_encoder` — cùng engine FastAPI dùng cho ``response_model`` —
để chuyển UUID, ``datetime``, ``Enum``, ``BaseModel`` lồng nhau, ``set``, v.v. thành kiểu JSON-safe.
"""

from __future__ import annotations

from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def to_jsonable(value: Any) -> Any:
    """Chuẩn bị dữ liệu cho JSON (một chỗ nếu sau này cần tuỳ biến thêm)."""
    return jsonable_encoder(value)


class SafeJSONResponse(JSONResponse):
    """
    Giống ``JSONResponse`` nhưng encode ``content`` qua ``jsonable_encoder`` trước khi serialize.

    Truyền trực tiếp ``BaseModel`` hoặc dict có ``uuid.UUID`` — không cần gọi ``model_dump(mode=\"json\")``.
    """

    def __init__(self, content: Any, status_code: int = 200, **kwargs: Any) -> None:
        super().__init__(content=to_jsonable(content), status_code=status_code, **kwargs)
