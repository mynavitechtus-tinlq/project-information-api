from fastapi import APIRouter, status
from pydantic import BaseModel

from app.schemas.response.success import SuccessResponse

router = APIRouter(tags=["Health"])


class HealthCheckData(BaseModel):
    status: str


@router.get(
    "/health",
    summary="Health Check",
    operation_id="health_check",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse[HealthCheckData],
)
async def health_check():
    return SuccessResponse[HealthCheckData](data=HealthCheckData(status="ok"))
