from collections import namedtuple

ExceptionData = namedtuple("ExceptionData", ["detail", "code"])


USER_NOT_REGISTERED = ExceptionData(
    detail="Данный пользователь не зарегистрирован", code="user_not_registered"
)
USER_IS_REGISTERED = ExceptionData(
    detail="Данный пользователь уже зарегистрирован", code="user_is_registered"
)
NO_TELEGRAM_DATA = ExceptionData(
    detail="У данного пользователя нет данных Телеграмм", code="no_telegram_data"
)
USER_IS_BLOCKED = ExceptionData(
    detail="Пользователь заблокирован", code="user_is_blocked"
)
NOT_VALID_PAYMENT_METHOD = ExceptionData(
    detail="Данный способ оплаты не поддерживается", code="not_valid_payment_method"
)
INSUFFICIENT_FUNDS = ExceptionData(
    detail="Недостаточно средств", code="insufficient_funds"
)
UNKNOWN_PAYMENT_ERROR = ExceptionData(
    detail="Неизвестная ошибка при оплате", code="unknown_payment_error"
)
USER_IS_NOT_DRIVER = ExceptionData(
    detail="Пользователь не имеет прав водителя", code="user_is_not_driver"
)
DRIVER_ALREADY_WORKING = ExceptionData(
    detail="Водитель уже вышел на линию", code="driver_already_working"
)
