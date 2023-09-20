from pathlib import Path

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs

BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
env.read_env()

DEBUG = env.bool("DEBUG")

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
DADATA_TOKEN = env.str("DADATA_TOKEN")
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов

for i in range(len(ADMINS)):
    ADMINS[i] = int(ADMINS[i])

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
WEB_BOT_URL = env.str("WEB_BOT_URL")

# webhook settings
CORE_TOKEN = env.str("CORE_TOKEN")
if DEBUG:
    WEBHOOK_HOST = env.str("WEBHOOK_HOST")
else:
    WEBHOOK_HOST = env.str("WEBHOOK_HOST_TEST")
# if DEBUG:
#     WEBHOOK_PATH = '/'+ CORE_TOKEN + '/'
# else:
#     WEBHOOK_PATH = '/_telegram_bot/' + CORE_TOKEN + '/'

WEBHOOK_PATH = "/_telegram_bot/" + CORE_TOKEN + "/"

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

QIWI_WEBHOOK_PATH = f"{WEBHOOK_PATH}" + "qiwi/"
QIWI_WEBHOOK_URL = f"{WEBHOOK_HOST}{QIWI_WEBHOOK_PATH}"

MAILING_WEBHOOK_PATH = f"{WEBHOOK_PATH}" + "mailing/"
ORDER_REVISION_NOTIFY_WEBHOOK_PATH = WEBHOOK_PATH + "orderRevisionNotify/"

# webserver settings
WEBAPP_HOST = IP
WEBAPP_PORT = env.int("port")


CORE_TOKEN = env.str("CORE_TOKEN")
QIWI_TOKEN = env.str("QIWI_TOKEN")
QIWI_PHONE_NUMBER = env.str("QIWI_PHONE_NUMBER")

BASE_URL = env.str("CORE_BASE_URL")
CORE_BASE_URL = BASE_URL + "/api/"
CORE_HEADERS = {}

CABINET_LOGIN_URL = env.str("CABINET_LOGIN_URL")

MEDIA_URL = BASE_DIR / "data/media/"
ICONS_MEDIA_URL = MEDIA_URL / "telegram_icons"
LOGGING_FILE_PATH = BASE_DIR / "data" / "logs" / "logging.log"


REDIS_NAME = "redis"
REDIS_PORT = 6379
REDIS_LOCATION_DB = 1
REDIS_FSM_DB = 2
# !!! 3 db number занят ядром, если находятся на одном сервере
REDIS_PASSWORD = "foobared"

DRIVER_LOCATION_PREFIX = "dl"

UPDATE_DRIVER_LOCATION_PERIOD = 5
UPDATE_DRIVER_LOCATION_LOGGER_ID = "UPDATE_LOCATION"
UPDATE_DRIVER_LOCATION_FILE = BASE_DIR / "data" / "logs" / "update_locations.log"
QIWI_LOGGER_ID = "QIWI_LOGGER"
QIWI_LOGGER_FILE = BASE_DIR / "data" / "logs" / "qiwi.log"

DEFAULT_LIVE_PERIOD = 7200
