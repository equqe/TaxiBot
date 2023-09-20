from aiogram import types
from aiogram.dispatcher import FSMContext

from data.buttons import EXIT
from handlers.users.main_menu import main_menu_handler
from loader import dp


# Хэндлер принимает сообщения для выхода из состояния и открывает главное меню
@dp.message_handler(lambda message: message.text.lower() == EXIT.lower(), state="*")
async def exit_from_state(message: types.Message, state: FSMContext = None):
    await state.finish()
    return await main_menu_handler(message, state)


@dp.callback_query_handler(text=EXIT, state="*")
async def exit_from_state_callback_handler(
    call: types.CallbackQuery, state: FSMContext = None
):
    await state.finish()
    await main_menu_handler(
        None, state, chat_id=call.from_user.id, pre_text="Хорошо, закрываю. "
    )
