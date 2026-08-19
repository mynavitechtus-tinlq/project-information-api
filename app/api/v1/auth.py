from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.constants.messages import ErrorMessage
from app.core.depends.providers import get_auth_service
from app.schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    summary="Login",
    operation_id="login",
    response_model=LoginResponse,
)
async def login(payload: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    data = await auth_service.login(str(payload.email).strip(), payload.password)
    return LoginResponse(data=data)


@router.post(
    "/refresh",
    summary="Refresh access token",
    operation_id="refresh_access_token",
    response_model=LoginResponse,
)
async def refresh_access_token(
    payload: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    data = await auth_service.refresh_access_token(payload.refresh_token.strip())
    return LoginResponse(data=data)


@router.delete(
    "/logout",
    summary="Logout",
    operation_id="logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    auth_service: AuthService = Depends(get_auth_service),
):
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessage.MISSING_CREDENTIALS.message)

    await auth_service.logout(credentials.credentials)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
