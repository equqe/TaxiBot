from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import Union

from data.buttons import SEND_LOCATION, SEND_PHONE_NUMBER, EXIT, WRITE_ADDRESS


async def request_data_keyboard(
    buttons: Union[list, tuple] = [], exit=True
) -> ReplyKeyboardMarkup:
    """
    Возвращает клавиатуры для отправки геопозиции
    """
    keyboard = ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True
    )
    if "location" in buttons:
        keyboard.add(KeyboardButton(text=SEND_LOCATION, request_location=True))
    elif "phone" in buttons:
        keyboard.add(KeyboardButton(text=SEND_PHONE_NUMBER, request_contact=True))

    if "address" in buttons:
        keyboard.add(KeyboardButton(WRITE_ADDRESS))

    if exit:
        keyboard.add(KeyboardButton(text=EXIT))

    return keyboard
