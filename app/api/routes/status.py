from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["status"])

@router.get("/status")
def status():
    logger.info("Status: API Called")
    return {"status" : "online", "version":"0.0.1"}