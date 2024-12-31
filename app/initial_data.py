import logging
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy import Engine
from app.core.db import postgres_engine, userdb_engine
from sqlalchemy import text
from app.core.config import settings
from app.models.user import Base

logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def initDb(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
            logger.info("Bootup initDb : db awake")
    except Exception as e:
        logger.error(e)
        raise e
    
def create_user_database_if_not_exists():
    """
    Connect to `postgres` database and create `userdb` if it does not exist.
    """
    with postgres_engine.connect() as connection:
        connection = connection.execution_options(isolation_level="AUTOCOMMIT")
        result = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": settings.USER_DB}
        ).fetchone()

        if not result:
            connection.execute(text(f"CREATE DATABASE {settings.USER_DB}"))
            logger.info(f"Database '{settings.USER_DB}' created.")
        else:
            logger.info(f"Database '{settings.USER_DB}' already exists.")
            # Create all tables
            logger.info(f"Database '{settings.USER_DB}' creating user tables.")
            Base.metadata.create_all(bind=userdb_engine)
            logger.info(f"Database '{settings.USER_DB}' created user tables.")
    
# Service BootUp 
# DB Creation and Table Migrations
def service_boot_up():
    initDb(postgres_engine)
    create_user_database_if_not_exists()