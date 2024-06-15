import logging

from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG["loggers"][__name__] = {
    "handlers": ["default"],
    "level": "INFO",
    "propagate": False,
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
