import logging
from logging.handlers import RotatingFileHandler


from data.config import (
    LOGGING_FILE_PATH,
    QIWI_LOGGER_FILE,
    QIWI_LOGGER_ID,
    UPDATE_DRIVER_LOCATION_FILE,
    UPDATE_DRIVER_LOCATION_LOGGER_ID,
    DEBUG,
)

_logging_format = (
    "%(levelname)-8s | %(filename)s | %(funcName)s() [%(asctime)s]  %(message)s"
)
logging_format = logging.Formatter(_logging_format)


if not DEBUG:

    logger_handler = RotatingFileHandler(
        LOGGING_FILE_PATH, maxBytes=1024 * 1024 * 10, backupCount=5
    )
else:
    logger_handler = logging.StreamHandler()

logger_handler.setFormatter(logging_format)


logging.basicConfig(
    format=_logging_format,
    level=logging.DEBUG
    if DEBUG
    else logging.INFO,  # Можно заменить на другой уровень логгирования.,
    handlers=[logger_handler],
)

logger = logging.getLogger("main")
logger.addHandler(logger_handler)

# QIWI Logging file
qiwi_logger = logging.getLogger(QIWI_LOGGER_ID)
qiwi_handler = RotatingFileHandler(
    QIWI_LOGGER_FILE, maxBytes=1024 * 1024 * 10, backupCount=5
)
qiwi_handler.setFormatter(logging_format)
qiwi_logger.addHandler(qiwi_handler)


update_locations_logger = logging.getLogger(UPDATE_DRIVER_LOCATION_LOGGER_ID)
update_location_handler = RotatingFileHandler(
    UPDATE_DRIVER_LOCATION_FILE, maxBytes=1024 * 1024 * 5, backupCount=2
)
update_location_handler.setFormatter(logging_format)
update_locations_logger.addHandler(update_location_handler)
