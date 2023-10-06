import asyncio
import logging

from aiogram import executor
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

import filters
import handlers
import middlewares  # Нужно
from data.config import (
    MAILING_WEBHOOK_PATH,
    ORDER_REVISION_NOTIFY_WEBHOOK_PATH,
    QIWI_LOGGER_ID,
    QIWI_WEBHOOK_PATH,
    UPDATE_DRIVER_LOCATION_PERIOD,
    WEBAPP_HOST,
    WEBAPP_PORT,
    WEBHOOK_PATH,
    WEBHOOK_URL,
)
from data.texts import DRIVERS_HAD_FOUNDED
from keyboards.inline.order import (
    create_order_revision_keyboard,
    revision_order_keyboard,
)
from loader import bot, core, dp, qiwi
from models.referral import Mailing
from utils import get_payload_data
from utils.checks import check_qiwi_payload
from utils.mailing import message_to_user_list
from utils.misc.logging import logger
from utils.notify_admins import on_startup_notify
from utils.stop_session import stop_session
from utils.tasks.update_driver_locations import update_user_locations

app = web.Application()
routes = web.RouteTableDef()

qiwi_logger = logging.getLogger(QIWI_LOGGER_ID)


@routes.post(QIWI_WEBHOOK_PATH)
async def qiwi_webhook(request: Request):
    payload = await request.json()
    payment_id = payload.get("payment").get("txnId")
    qiwi_logger.info(f'{"-"*10}\nNew QIWI operation {payment_id=}')
    is_valid = check_qiwi_payload(payload, qiwi.webhook_key)
    if is_valid:
        qiwi_logger.info(f"QIWI operation is valid {payment_id=}")
        payload_data = await get_payload_data(payload)
        qiwi_logger.info("Данные успешно обработаны")
        user = await core.update_user_balance(
            user_id=payload_data.user_id, value=payload_data.value
        )
        await bot.send_message(
            chat_id=user.telegram_data.chat_id,
            text=f"Зачисление на ваш баланс с QIWI-кошелька: <b>{payload_data.value} руб.</b>\n\n<b>Сумма на балансе:</b> {user.balance.money} руб.",
        )
        qiwi_logger.info(
            f"Баланс пользователя {payload_data.user_id} успешно обновлён!"
        )
        return Response(status=200, text="ok")
    else:
        qiwi_logger.warning(f"QIWI operation is invalid: {payload}")


print(f"{MAILING_WEBHOOK_PATH=}")


@routes.post(MAILING_WEBHOOK_PATH)
async def mailing_webhook(request: Request):
    """
    Принимает запрос на рассылку и начинает рассылку
    """
    payload = await request.json()
    mailing = Mailing.parse_obj(payload)
    logger.info(f"Новая рассылка: {mailing}")

    await message_to_user_list(
        user_list=mailing.telegram_ids,
        text=mailing.message.text,
        photo=mailing.message.photo_url,
        video=mailing.message.video_url,
        url=mailing.message.url,
        url_button_name=mailing.message.url_button_name,
        **mailing.message.get_message_kwargs(),
    )
    logger.info("Рассылка завершена!")
    return Response(status=200, text="ok")


print(f"{ORDER_REVISION_NOTIFY_WEBHOOK_PATH=}")


@routes.post(ORDER_REVISION_NOTIFY_WEBHOOK_PATH)
async def order_revision_check_handler(request: Request):
    """
    Принимает заказы, в которых нашлись водители спустя время
    """
    payload = await request.json()
    success = payload["success"]
    failed = payload["failed"]

    for revision in success:
        chat_id = revision.get("chat_id")
        order_id = revision.get("order_id")
        await bot.send_message(
            chat_id,
            DRIVERS_HAD_FOUNDED,
            reply_markup=await revision_order_keyboard(order_id),
        )

    for revision in failed:
        chat_id = revision.get("chat_id")
        order_id = revision.get("order_id")
        await bot.send_message(
            chat_id,
            "К сожалению, я не смог найти водителей. Администрация уведомлена об этой проблеме и будет нанимать больше водителей. Нажмите на кнопку ниже, чтобы снова включить поиск.",
            reply_markup=await create_order_revision_keyboard(order_id=order_id),
        )

    return Response(status=200, text="ok")


async def update_user_locations_task():
    while True:
        try:
            await update_user_locations()
        except Exception as E:
            logger.warning(f"Не удалось обновить геопозицию водителей {E.args}")
        await asyncio.sleep(UPDATE_DRIVER_LOCATION_PERIOD)


async def on_startup(dispatcher):
    # Уведомляет про запуск
    # print("Start set webhook")
    # await bot.set_webhook(WEBHOOK_URL)
    # try:
    #     qiwi.delete_webhook()
    # except Exception:
    #     pass
    # qiwi.set_webhook()
    # print("End set webhook")
    await core.start_session()
    # await on_startup_notify(dispatcher)
    loop = asyncio.get_running_loop()
    loop.create_task(update_user_locations_task())


async def on_shutdown(dispatcher):
    """
            Активирутеся при выключении
    :param dispatcher:
    :return:
    """
    await stop_session()
    await bot.delete_webhook()
    qiwi.delete_webhook()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# Чтобы не ругался
__noinspection_pycharm__ = (filters, handlers, middlewares)
if __name__ == "__main__":
    app.add_routes(routes)

    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    print(f"{WEBHOOK_PATH=}")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # e = executor.set_webhook(
    #     dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     web_app=app,
    # )
    # e.run_app(host=WEBAPP_HOST, port=WEBAPP_PORT)
