import jwt
import app.crud as crud
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from app.core.config import settings
from collections.abc import Generator
from sqlmodel import Session
from app.models.user import TokenPayload, User
from fastapi import Depends, HTTPException, status
import app.core.security as security
from app.core.db import userdb_engine
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/signin"
)

def get_db() -> Generator[Session, None, None]:
    with Session(userdb_engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.get_user_by_id(session=session, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]