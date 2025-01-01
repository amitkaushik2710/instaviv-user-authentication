import logging
logger = logging.getLogger(__name__)

from app.api.deps import (
    CurrentUser,
)

from fastapi import APIRouter
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/details")
def user_details(current_user: CurrentUser):
    logger.info("user_details: API Called")
    logger.info(f"user_details: user : {current_user}")
    return {"status" : 200 , "user_details" : current_user.email}

