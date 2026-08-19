from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.configs import settings


def create_sql_engine(is_async=True) -> AsyncEngine:
    prefix = "postgresql://"
    connect_args = {"connect_timeout": settings.DB_CONNECT_TIMEOUT}
    engine_func = create_engine

    if is_async:
        prefix = "postgresql+asyncpg://"
        connect_args = {"timeout": settings.DB_ASYNC_TIMEOUT}
        engine_func = create_async_engine

    return engine_func(
        prefix + settings.DATABASE_URL,
        connect_args=connect_args,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_size=settings.DB_POOL_SIZE,
    )


async_engine = create_sql_engine()
async_session_factory = async_sessionmaker(
    async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a request-scoped async SQLAlchemy session."""
    async with async_session_factory() as session:
        yield session


class SessionLocal:
    _instance = None
    session_factory: async_sessionmaker[AsyncSession]

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SessionLocal, cls).__new__(cls)
            cls._instance._init_session()
        return cls._instance

    @classmethod
    def _init_session(cls):
        cls.session_factory = async_session_factory
