import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from loader import dp

from data.config import ADMINS, LOGGING_FILE_PATH


@dp.message_handler(Command("logs"), state="*")
async def send_logs_handler(message: types.Message, state: FSMContext = None):
    """
    Send logs to user, only for admins
    """
    logging.info("Запрос логов пользователем: %s" % message.from_user.id)
    if message.from_user.id not in ADMINS:
        logging.info("Проверка не пройдена")
        return
    logging.info("Проверка пройдена!")
    logfile = types.InputFile(LOGGING_FILE_PATH)
    await message.answer_document(logfile)
