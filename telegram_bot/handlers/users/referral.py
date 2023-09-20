from aiogram import types

from data.buttons import REFERRAL_PROGRAM
from loader import dp, bot
from middlewares.authentication import authenticate
from models.cabinet import User
from data.texts import REFERRAL_MAIN_TEXT
from keyboards.inline import referral_keyboard


@dp.message_handler(text=REFERRAL_PROGRAM)
@authenticate()
async def referral_program_handler(message: types.Message):
    """
    Отправляет сообщение с информацией о реферальной программе
    """
    user: User = message.user
    bot_username = (await bot.me).username
    link = user.generate_referral_link(bot_username=bot_username)
    await message.answer(
        REFERRAL_MAIN_TEXT.format(referral_link=link),
        reply_markup=await referral_keyboard(url=link),
    )
