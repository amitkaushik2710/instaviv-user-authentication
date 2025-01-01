from fastapi import APIRouter

from app.api.routes import status, register_user, signin, user_details

api_router = APIRouter()
api_router.include_router(status.router)
api_router.include_router(register_user.router)
api_router.include_router(signin.router)
api_router.include_router(user_details.router)
