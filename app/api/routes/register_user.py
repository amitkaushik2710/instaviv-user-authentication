from fastapi import APIRouter, HTTPException
from app.api.deps import (
    SessionDep,
)
import app.crud as crud
from app.models.user import UserReq
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup")
def register_user(session: SessionDep, user: UserReq) -> None:
    logger.info("register_user: API Called")

    logger.info(f"register_user: request user : {user}")

    if not user.email or not user.password:
        raise HTTPException(
            status_code=400,
            detail="user email or password is empty",
        )

    userdb = crud.get_user_by_email(session=session, email=user.email)
    logger.info(f"register_user: db user : {userdb}")
    if userdb:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    user = crud.create_user(session=session, user=user)

    return {"status" : 200 , "message" : "user created successfully"}