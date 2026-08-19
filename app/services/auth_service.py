from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.constants.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH
from app.core.constants.messages import ErrorMessage
from app.helpers.password_hash import verify_password
from app.helpers.utc_datetime import as_utc_aware, utc_now_naive
from app.helpers.token_decode import token_decode
from app.helpers.token_encode import token_encode
from app.models.user_model import Users
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth import LoginData


class AuthService:
    def __init__(self, user_repository: UserRepository, session_repository: UserSessionRepository):
        self.user_repository = user_repository
        self.session_repository = session_repository

    def _create_tokens(self, user: Users) -> tuple[str, str, datetime, datetime]:
        access_payload = {
            "user_id": str(user.id),
            "email": user.email,
            "username": user.username,
        }
        access_token = token_encode(access_payload, token_type=TOKEN_TYPE_ACCESS)

        refresh_payload = {"user_id": str(user.id)}
        refresh_token = token_encode(refresh_payload, token_type=TOKEN_TYPE_REFRESH)

        now = utc_now_naive()
        access_expires = now + self._access_token_lifetime()
        refresh_expires = now + self._refresh_token_lifetime()

        return access_token, refresh_token, access_expires, refresh_expires

    @staticmethod
    def _access_token_lifetime() -> timedelta:
        from app.core.configs import settings

        return timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)

    @staticmethod
    def _refresh_token_lifetime() -> timedelta:
        from app.core.configs import settings

        return timedelta(seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS)

    async def authenticate_user(self, email: str, password: str) -> Users | None:
        user = await self.user_repository.get_user_by_email(email)
        if user is None or not user.is_active:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    async def get_active_user_by_id(self, user_id: UUID) -> Users | None:
        user = await self.user_repository.get_item_by_id(user_id)
        if user is None or not user.is_active:
            return None
        return user

    async def login(self, email: str, password: str) -> LoginData:
        user = await self.authenticate_user(email, password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        access_token, refresh_token, access_expires_at, refresh_expires_at = self._create_tokens(user)

        await self.session_repository.create_session(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_expires_at,
            refresh_token_expires_at=refresh_expires_at,
        )

        return LoginData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=as_utc_aware(access_expires_at),
            refresh_expires_at=as_utc_aware(refresh_expires_at),
        )

    async def refresh_access_token(self, refresh_token: str) -> LoginData:
        try:
            decoded = token_decode(refresh_token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.EXPIRED_CREDENTIALS.message,
            ) from None
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            ) from None

        if decoded.get("type") != TOKEN_TYPE_REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        user_id_str = decoded.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        session = await self.session_repository.get_by_refresh_token(refresh_token)
        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        try:
            user_uuid = UUID(str(user_id_str))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            ) from None

        if session.user_id != user_uuid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        user = await self.get_active_user_by_id(session.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessage.AUTHORIZATION_ERROR.message,
            )

        await self.session_repository.delete_session_by_access_token(session.access_token)

        access_token, new_refresh, access_expires_at, refresh_expires_at = self._create_tokens(user)

        await self.session_repository.create_session(
            user_id=user.id,
            access_token=access_token,
            refresh_token=new_refresh,
            access_token_expires_at=access_expires_at,
            refresh_token_expires_at=refresh_expires_at,
        )

        return LoginData(
            access_token=access_token,
            refresh_token=new_refresh,
            expires_at=as_utc_aware(access_expires_at),
            refresh_expires_at=as_utc_aware(refresh_expires_at),
        )

    async def logout(self, access_token: str) -> None:
        try:
            decoded = token_decode(access_token)
        except (ExpiredSignatureError, InvalidTokenError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            ) from None

        if decoded.get("type") != TOKEN_TYPE_ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        user_id_str = decoded.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            )

        session = await self.session_repository.get_by_access_token(access_token)
        if session is not None:
            await self.session_repository.delete_session_by_access_token(access_token)
            return

        try:
            user_id = UUID(str(user_id_str))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.INVALID_CREDENTIALS.message,
            ) from None

        await self.session_repository.delete_all_for_user(user_id)
