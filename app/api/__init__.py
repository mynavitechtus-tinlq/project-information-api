from fastapi import APIRouter

from app.api.v1 import router

routes = APIRouter(prefix="/api")

routes.include_router(router)
