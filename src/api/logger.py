from loguru import logger
import sys

from api.constants import ENV, LOG_LEVEL, LOGS_DIR

LOGS_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(
    sys.stdout,
    level="CRITICAL" if ENV == "TEST" else LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

if ENV != "TEST":
    logger.add(
        LOGS_DIR / "app_{time:YYYY-MM-DD_HH}.log",
        level=LOG_LEVEL,
        rotation="4 hours",
        retention="7 days",
        compression="gz",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )
