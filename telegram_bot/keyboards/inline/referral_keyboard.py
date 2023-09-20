from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.texts import REFERRAL_INVITE_TEXT


async def referral_keyboard(url):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Пригласить друга",
            switch_inline_query=REFERRAL_INVITE_TEXT.format(referral_link=url),
        )
    )
    return keyboard
