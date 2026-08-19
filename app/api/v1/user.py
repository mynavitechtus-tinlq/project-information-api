from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.constants.messages import ErrorMessage
from app.core.depends.providers import get_user_service
from app.core.depends.validate_token import get_current_user
from app.helpers.safe_json_response import SafeJSONResponse
from app.schemas.entities.user import UserModel
from app.schemas.response.success import PaginatedData, PaginationMeta, SuccessResponse
from app.services.user_service import UserService

router = APIRouter(tags=["User"])


@router.get(
    "/users",
    summary="Get users",
    operation_id="get_users",
    response_model=SuccessResponse[PaginatedData[UserModel]],
    dependencies=[Depends(get_current_user)],
)
async def get_users(
    page: int = Query(default=1, ge=1, description="Current page number (1-based)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    user_service: UserService = Depends(get_user_service),
):
    users, total_items = await user_service.get_all_users_paginated(page=page, page_size=page_size)
    total_pages = (total_items + page_size - 1) // page_size if total_items else 0

    response_data = PaginatedData[UserModel](
        items=users,
        pagination=PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        ),
    )

    return SafeJSONResponse(
        status_code=status.HTTP_200_OK,
        content=SuccessResponse[PaginatedData[UserModel]](data=response_data),
    )


@router.get(
    "/users/{item_id}",
    summary="Get user by id",
    operation_id="get_user_by_id",
    response_model=SuccessResponse[UserModel],
    dependencies=[Depends(get_current_user)],
)
async def get_user(item_id: UUID, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user(item_id)
    if not user:
        raise HTTPException(status_code=404, detail=ErrorMessage.USER_NOT_FOUND.message)
    return SafeJSONResponse(
        status_code=status.HTTP_200_OK,
        content=SuccessResponse[UserModel](data=user),
    )
