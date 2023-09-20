from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.buttons import USE_COUPON_LATER
from models.referral import Coupon

cb = CallbackData("coupon", "pk")


async def pick_coupons_keyboard(coupons: List[Coupon]) -> InlineKeyboardMarkup:
    """
    Возвращает инлайн клавиатуру для выбора скидочного купона при оформлении заказа
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = (
        InlineKeyboardButton(text=coupon.name, callback_data=cb.new(pk=coupon.id))
        for coupon in coupons
    )
    keyboard.add(*buttons)
    # Пропуск шага
    keyboard.insert(
        InlineKeyboardButton(text=USE_COUPON_LATER, callback_data=cb.new(pk="-"))
    )

    return keyboard
