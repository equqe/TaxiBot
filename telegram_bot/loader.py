import asyncio

from aiogram import Bot, Dispatcher, types

from api.main import CoreAPI
from data import config
from data.config import (
    DRIVER_LOCATION_PREFIX,
    QIWI_PHONE_NUMBER,
    QIWI_TOKEN,
    REDIS_FSM_DB,
    REDIS_LOCATION_DB,
    REDIS_NAME,
    REDIS_PASSWORD,
    REDIS_PORT,
)
from utils.aioredis_storage import RedisStorage
from utils.misc.qiwi_wallet import Wallet, WalletMock
from utils.misc.upgraded_storage import RedisPickleFSMStorage
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
FSMStorage = RedisPickleFSMStorage(
    REDIS_NAME, REDIS_PORT, REDIS_FSM_DB, prefix="fsm", password=REDIS_PASSWORD
)
dp = Dispatcher(bot, storage=FSMStorage, loop=asyncio.get_event_loop())
core = CoreAPI(
    token=config.CORE_TOKEN, base_url=config.CORE_BASE_URL, headers=config.CORE_HEADERS
)

location_storage = RedisStorage(
    db_name=REDIS_NAME,
    db_port=REDIS_PORT,
    db_number=REDIS_LOCATION_DB,
    password=REDIS_PASSWORD,
    prefix=DRIVER_LOCATION_PREFIX,
)

if not config.DEBUG:
    qiwi = Wallet(token=QIWI_TOKEN, number=QIWI_PHONE_NUMBER)
else:
    qiwi = WalletMock(number=123)
