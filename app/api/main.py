from fastapi import APIRouter

from app.api.routes import status, register_user
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(status.router)
api_router.include_router(register_user.router)
