import logging
from collections import namedtuple

from data.config import QIWI_LOGGER_ID

PaymentData = namedtuple("PaymentData", ["payment_id", "user_id", "value", "date"])

qiwi_logger = logging.getLogger(QIWI_LOGGER_ID)


async def get_payload_data(payload: dict) -> PaymentData:
    payment = payload["payment"]
    payment_id = payment["txnId"]
    try:
        user_id = int(payment["comment"])
    except ValueError as E:
        qiwi_logger.warning(f"Ошибка обработки данных платежа #{payment_id}: {E.args}")
        raise ValueError
    if payment["sum"]["currency"] == 643:
        value = payment["sum"]["amount"]
    else:
        qiwi_logger.exception(
            f"В платеже {payment_id=} указана неверная валюта, платёж не обработан."
        )
    date = payment["date"]

    return PaymentData(payment_id, user_id, value, date)
