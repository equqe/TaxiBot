from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from loader import dp
from utils.mailing import message_to_user_list


@dp.message_handler(Command("test"))
async def bot_test(message: types.Message):
    await message_to_user_list(user_list=[message.from_user.id], text="123")
