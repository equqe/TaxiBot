from aiogram.dispatcher.filters.state import State, StatesGroup


class DriverMenu(StatesGroup):
    """
    Меню для водителей
    """

    order_in_progress = State()


class OrderStateDriver(StatesGroup):

    order_start = State()