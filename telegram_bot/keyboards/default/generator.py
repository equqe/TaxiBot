from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def generator(*args, row_width=1, resize_keyboard=True) -> ReplyKeyboardMarkup:
    """
    Генератор кнопок, тексты передаются в аргументах
    """
    keyboard = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
    buttons = (KeyboardButton(text) for text in args)
    keyboard.add(*buttons)

    return keyboard
