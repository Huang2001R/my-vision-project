from loguru import logger
import sys
from pathlib import Path

from app.config.settings import settings

def setup_logger():
    logger.remove()
    
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.log_level,
        colorize=True
    )
    
    logger.add(
        str(settings.log_file),
        format=log_format,
        level=settings.log_level,
        rotation="1 week",
        retention="1 month"
    )
    
    return logger

logger = setup_logger()
