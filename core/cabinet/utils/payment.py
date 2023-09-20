from rest_framework.exceptions import ParseError

from cabinet.exceptions import NOT_VALID_PAYMENT_METHOD
from cabinet.settings import PAYMENT_METHODS


def payment(user, payment_method: str, value):
    # Проверка способа оплаты
    is_valid = check_payment_method(payment_method)


def check_payment_method(payment_method: str, raise_exception=True) -> bool:
    # Проверяет способ оплаты
    status = None
    for _, code in PAYMENT_METHODS:
        if not status:
            if code == payment_method:
                status = True
    if not status and raise_exception:
        ParseError(NOT_VALID_PAYMENT_METHOD.code)
    return status
