import pyqiwi
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.buttons import (
    EXIT,
    TOP_UP_BALANCE,
    START_WORK_DAY,
    FINISH_WORK_DAY,
    OPEN_DRIVER_CABINET,
)
from data.config import CABINET_LOGIN_URL
from loader import qiwi
from models.cabinet import User

cb = CallbackData("driver_menu", "action")


async def driver_cabinet_keyboard(
    user: User, out_line_cost=None, hide_driver_cabinet: bool = False
) -> InlineKeyboardMarkup:
    """
    Возвращает инлайн клавиатуру для выбора скидочного купона при оформлении заказа
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    if out_line_cost:
        payment_url = pyqiwi.generate_form_link(
            pid=99,
            account=qiwi.number,
            amount=200 if not out_line_cost else out_line_cost,
            comment=user.id,
            blocked=["account", "comment"],
        )
        keyboard.add(InlineKeyboardButton(TOP_UP_BALANCE, url=payment_url))

    if user.driver.is_active:
        keyboard.add(
            InlineKeyboardButton(FINISH_WORK_DAY, callback_data=cb.new(FINISH_WORK_DAY))
        )
    else:
        keyboard.add(
            InlineKeyboardButton(START_WORK_DAY, callback_data=cb.new(START_WORK_DAY))
        )
    if not hide_driver_cabinet:
        keyboard.insert(
            InlineKeyboardButton(
                text=OPEN_DRIVER_CABINET,
                url=CABINET_LOGIN_URL % user.telegram_auth_token,
            )
        )
    keyboard.insert(InlineKeyboardButton(text=EXIT, callback_data=cb.new(EXIT)))

    return keyboard
