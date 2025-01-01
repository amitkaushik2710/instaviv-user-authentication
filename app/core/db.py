from sqlmodel import create_engine
from app.core.config import settings
from sqlalchemy.ext.declarative import declarative_base

postgres_engine = create_engine(
    str(settings.SQLALCHEMY_POSTGRES_DATABASE_URI)
)

userdb_engine = create_engine(
    str(settings.SQLALCHEMY_USER_DATABASE_URI)
)

Base = declarative_base()