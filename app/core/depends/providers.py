"""Shared dependency providers for repositories and services."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.database import get_session
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService


# ============================================================
# Repository providers
# - Build repository instances from request-scoped dependencies.
# ============================================================
def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    """Build a request-scoped user repository."""
    return UserRepository(session=session)


def get_user_session_repository(session: AsyncSession = Depends(get_session)) -> UserSessionRepository:
    """Build a request-scoped user session repository."""
    return UserSessionRepository(session=session)


# ============================================================
# Service providers
# - Compose business services from one or more repositories.
# ============================================================
def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> UserService:
    """Build a request-scoped user service."""
    return UserService(user_repository=user_repository)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    session_repository: UserSessionRepository = Depends(get_user_session_repository),
) -> AuthService:
    """Build a request-scoped auth service."""
    return AuthService(user_repository=user_repository, session_repository=session_repository)
