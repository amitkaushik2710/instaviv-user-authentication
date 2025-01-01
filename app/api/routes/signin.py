import logging
logger = logging.getLogger(__name__)

from typing import Annotated
from datetime import timedelta

from app.core.config import settings
import app.crud as crud
from app.core import security
from app.models.user import Token
from app.api.deps import (
    SessionDep,
)

from fastapi import APIRouter, HTTPException,  Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signin")
def signin(
    session: SessionDep, req: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    logger.info("signin: API Called")
    logger.info(f"signin: request user : {req}")

    user = crud.authenticate(
        session=session, email=req.username, password=req.password
    )
    if not user:
        logger.error(f"signin: incorrect email or password {req}")
        raise HTTPException(
            status_code=400, 
            detail={
                "status_code": 400,
                "message": "incorrect email or password",
            },
        )
    logger.info(f"signin: got user from the db for request : {user}")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(weeks=settings.REFRESH_TOKEN_EXPIRE_WEEKS)
    access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    refresh_token=security.create_access_token(
            user.id, expires_delta=refresh_token_expires
        )
    token = Token(
        access_token=access_token,
        access_token_expires=access_token_expires.total_seconds(),
        refresh_token=refresh_token,
        refresh_token_expires=refresh_token_expires.total_seconds(),
        ) 
    response = JSONResponse(content=token.model_dump())
    response.set_cookie(
        key="tokens", 
        value=token, 
        httponly=True, 
        max_age=604800,
        secure=True, 
    )
    return response
    