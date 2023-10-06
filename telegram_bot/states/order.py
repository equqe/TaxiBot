from aiogram.dispatcher.filters.state import State, StatesGroup


ORDER_STATE = "OrderState"
PICK_START_LOCATION = "pick_start_location"
PICK_END_LOCATION = "pick_end_location"


class OrderState(StatesGroup):
    """
    Меню заказа такси
    """

    pick_start_location = State()
    pick_end_location = State()
    pick_baby_chair = State()
    pick_coupon = State()
    pick_payment_method = State()
    pick_phone_number = State()
    pick_price = State()
    get_comment_to_order = State()

    order_in_progress = State()


class OrderReviewState(StatesGroup):
    """
    Меню для оценки поездки
    """

    pick_stars = State()
    pick_text = State()


class OrderSity(StatesGroup):
    """
    Сохранение города поездки
    """

    sity = State()


