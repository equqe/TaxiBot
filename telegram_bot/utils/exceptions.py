class BaseException(Exception):
    """
    Базовый класс ошибки с кратким описанием и текстом,
    который должен быть отправлен пользователю.
    Для определения новых исключений наследовать его
    """

    default_detail = "Ошибка"
    default_message_text = (
        "Произошла неизвестная ошибка. Мы уже работаем над её исправлением!"
    )
    default_raise_exception = False

    def __init__(
        self, detail: str = None, message_text: str = None, raise_exception: bool = None
    ):
        """
        :param detail:          Содержание ошибки
        :param message_text:    Текст, который должен быть отправлен пользователю бота
        :param raise_exception: Нужно ли поднимать ошибку, если True, то в консоль выведется Traceback
        """
        self.detail = detail or self.default_detail
        self.message_text = message_text or self.default_message_text
        self.raise_exception = raise_exception or self.default_raise_exception


class UserNotFound(BaseException):
    """
    Пользователь не найден в API
    """

    default_message_text = "Вы не зарегистрированы в системе, пожалуйста, отправьте /start для автоматической регистрации."
    default_detail = "user_not_registered"


class UserIsBlocked(BaseException):
    default_message_text = "Вы заблокированы. Доступ запрещён."
    default_detail = "user_is_blocked"


class PaymentError(BaseException):
    default_message_text = (
        "Ошибка в системе оплаты. Возможно данный способ оплаты не поддерживается."
    )
    default_detail = "not_valid_payment_method"


class PermissionDenied(BaseException):
    """
    Пользователь не может выполнить данное действие
    """

    default_message_text = "У вас нет доступа к данной функции"
    default_detail = "permission_denied"


class InvalidCoreToken(BaseException):
    """
    Неверный токен или нет доступа
    """

    default_detail = "invalid_core_token"


class CoreError(BaseException):
    """
    Ошибка в ядре системы
    """

    default_message_text = (
        "Неизвестная ошибка в ядре системы. Мы уже работаем над её исправлением!"
    )
    default_detail = "core_error"


class UserIsRegistered(BaseException):
    """
    Пользовать уже зарегистрирован
    """

    default_message_text = "Вы уже зарегистрированы!"
    default_detail = "user_is_registered"


class BadCoreRequest(BaseException):
    """
    Ошибка в ядре системы
    """

    default_message_text = (
        "Ошибка в запросе в ядро системы. Мы уже работаем над её исправлением!"
    )
    default_detail = "bad_core_request"


class NoActionFound(BaseException):
    """
    Если пользователь выбрал действие, которое не поддерживается
    """

    default_message_text = "Возникла ошибка, данное действие не поддерживается системой. Мы уже работаем над её исправлением!"
    default_detail = "no_action_found"


class OrderError(BaseException):
    """
    Ошибка, связанная с заказом
    """

    default_message_text = "Произошла ошибка в системе диспетчера"
    default_detail = "order_error"


class OrderCanceledByClient(BaseException):
    """
    Заказ отменен клиентом
    """

    default_message_text = "Заказ отменён клиентом."
    default_detail = "order_canceled_by_client"
