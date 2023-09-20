from aiogram.dispatcher.filters.state import State, StatesGroup


class UpdatePhoneNumber(StatesGroup):
    is_active = State()
