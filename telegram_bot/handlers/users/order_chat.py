from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from loader import dp
from models.dispatcher import ACCEPTED, DRIVER_IS_WAITING, RIDE_IS_STARTED
from states import OrderState, DriverMenu


@dp.message_handler(
    state=OrderState.order_in_progress, content_types=types.ContentTypes.ANY
)
async def client_message_in_order_hanlder(message: types.Message, state: FSMContext):
    """
    Пересылает сообщения клиента водителю
    """

    data = await state.get_data()
    order = data.get("order")
    if order.status not in (ACCEPTED, DRIVER_IS_WAITING, RIDE_IS_STARTED):
        return
    driver_chat_id = order.driver.telegram_data.chat_id

    await message.send_copy(driver_chat_id)


@dp.message_handler(
    state=DriverMenu.order_in_progress, content_types=types.ContentTypes.ANY
)
async def driver_messages_in_ride_handler(message: types.Message, state: FSMContext):
    """
    Пересылает сообщения водителя клиенту
    """

    data = await state.get_data()
    ride = data.get("ride")
    client_chat_id = ride.client.telegram_data.chat_id

    await message.send_copy(client_chat_id)
