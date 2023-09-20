from utils.exceptions import (
    BaseException,
    OrderCanceledByClient,
    OrderError,
    PaymentError,
    PermissionDenied,
    UserIsBlocked,
    UserIsRegistered,
    UserNotFound,
)

#'Вы не зарегистрированы в системе. Пожалуйста отправьте /start, чтобы зарегистрироваться.'
# CORE_ERRORS[detail] = message_answer.text
CORE_ERRORS = {
    "no_telegram_data": UserNotFound,
    "user_is_registered": UserIsRegistered,
    "user_not_registered": UserNotFound,
    "user_is_blocked": UserIsBlocked,
    "not_valid_payment_method": PaymentError,
    "insufficient_funds": PaymentError(
        message_text="Недостаточно средств", detail="insufficient_funds"
    ),
    "unknown_payment_error": PaymentError(
        message_text="Произошла неизвестная ошибка в системе оплаты.",
        detail="unknown_payment_error",
    ),
    "user_is_not_driver": PermissionDenied(
        message_text="Произошла ошибка. Доступ к данной функции есть только у водителей.",
        detail="user_is_not_driver",
    ),
    "driver_already_working": PermissionDenied(
        message_text="Вы уже начали рабочий день!", detail="driver_already_working"
    ),
    "order_has_driver": OrderError(
        message_text="Заказ уже взял другой водитель!", detail="order_has_driver"
    ),
    "driver_already_has_order": OrderError(
        message_text="У вас уже есть активный заказ! Чтобы взять этот заказ, завершите предыдущий.",
        detail="driver_already_has_order",
    ),
    "this_driver_already_pick_this_order": OrderError(
        message_text="Вы уже взяли данный заказ!",
        detail="this_driver_already_pick_this_order",
    ),
    "city_not_registered": OrderError(
        message_text="К сожалению, я пока не работаю в вашем городе. Приходите позже!",
        detail="city_not_registered",
    ),
    "city_not_found": OrderError(
        message_text="Возникла ошибка, не удалось определить город по вашей геопозиции.",
        detail="city_not_found",
    ),
    "no_order": OrderError(
        message_text="Я не нашёл ваших активных заказов.", detail="no_order"
    ),
    "not_valid_order_status": OrderError(
        message_text="Невалидный статус заказа!", detail="not_valid_order_status"
    ),
    "client_already_has_order": OrderError(
        message_text="У вас уже создан 1 заказ!", detail="client_already_has_order"
    ),
    "order_canceled_by_client": OrderCanceledByClient,
    "coupon_does_not_exist": BaseException(
        message_text="Данного купона не существует!"
    ),
    "coupon_has_already_been_used": BaseException(
        message_text="Вы уже использовали данный купон!"
    ),
}
