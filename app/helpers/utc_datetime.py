"""UTC datetime helpers — một chỗ xử lý naive/aware cho Postgres ``TIMESTAMP WITHOUT TIME ZONE`` và JWT.

Quy ước dự án:

- **Ghi DB** (cột không timezone): dùng **naive UTC** — :func:`utc_now_naive`, :func:`to_naive_utc`.
- **So sánh / JWT** (epoch, logic): dùng **UTC aware** — :func:`utc_now_aware`, :func:`as_utc_aware`.

asyncpg lỗi khi trộn naive và aware; giữ các thao tác DB qua helper này để tránh lặp lại.
"""

from __future__ import annotations

from datetime import datetime, timezone


def utc_now_naive() -> datetime:
    """Thời điểm hiện tại — naive UTC, phù hợp ORM/SQLAlchemy ``DateTime`` không ``timezone=True``."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def utc_now_aware() -> datetime:
    """Thời điểm hiện tại — UTC aware, dùng so sánh hoặc tính JWT (``iat``/``exp``)."""
    return datetime.now(timezone.utc)


def as_utc_aware(dt: datetime) -> datetime:
    """Chuẩn hoá ``datetime`` từ DB (thường naive UTC) hoặc bất kỳ tz nào → UTC aware."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_naive_utc(dt: datetime) -> datetime:
    """Aware → naive UTC (ghi DB). Naive thì giữ nguyên (coi là UTC wall time đã lưu)."""
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(timezone.utc).replace(tzinfo=None)
