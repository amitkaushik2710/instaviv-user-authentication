import logging
logger = logging.getLogger(__name__)

import app.crud as crud
from app.models.user import UserReq
from app.api.deps import (
    SessionDep,
)

from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup")
def register_user(session: SessionDep, req: UserReq):
    logger.info("register_user: API Called")
    logger.info(f"register_user: request user : {req}")

    if not req.email or not req.password:
        logger.error(f"register_user: got empty username or password {req}")
        raise HTTPException(
            status_code=400,
            detail={
                "status_code": 400,
                "message": "Email or password is empty",
            },
        )

    userdb = crud.get_user_by_email(session=session, email=req.email)
    logger.info(f"register_user: existing user in the db : {userdb}")
    if userdb:
        logger.error(f"register_user: failed to create new user. user already exist with email {req}")
        raise HTTPException(
            status_code=400,
            detail={
                "status_code": 400,
                "message": "user already exist with email",
            },
        )
    
    user = crud.create_user(session=session, user=req)
    logger.info(f"register_user: new user created in db : {user}")

    return {"status" : 200 , "message" : "user created successfully"}