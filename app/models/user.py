from sqlalchemy import Column, String
from pydantic import BaseModel, EmailStr
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, password={self.password})>"

class UserReq(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    access_token_expires: float
    refresh_token: str
    refresh_token_expires: float
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None