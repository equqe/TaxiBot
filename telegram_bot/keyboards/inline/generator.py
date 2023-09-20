from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generator(row_width=1, *args) -> InlineKeyboardMarkup:
    """
    Генератор инлайн клавиатуры, все параметры кнопок передаются подряд, как аргументы
    """
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    buttons = (InlineKeyboardButton(button_data) for button_data in args)
    keyboard.add(*buttons)

    return keyboard
