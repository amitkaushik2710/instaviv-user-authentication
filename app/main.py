import logging

from app.core.config import settings
from app.api.main import api_router
from app.initial_data import service_boot_up

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("fastapi-app")

logger.info("Booting up ...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Service BootUp - DB creation and table migrations
service_boot_up()

app.include_router(api_router, prefix=settings.API_V1_STR)
