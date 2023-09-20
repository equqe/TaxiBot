import hashlib
import hmac
import logging

from data.buttons import WRITE_ADDRESS


def location_check(func):
    async def decorator(message, state=None):
        if not message.location:
            await message.answer(
                "В данный момент вы должны отправить геопозицию. "
                f"Только так мы можем с точностью определить ваше местоположение.\n\nВы можете нажать на кнопку «{WRITE_ADDRESS}» и ввести адрес вручную 😉"
            )
            return
        return await func(message, state)

    return decorator


def check_qiwi_payload(json_data: dict, webhook_key: str) -> bool:
    payment = json_data.get("payment")
    sign_fields = payment.get("signFields").split(",")
    hash_key = json_data.get("hash")
    for i in range(len(sign_fields)):
        fields = sign_fields[i].split(".")
        if len(fields) == 2:
            field1 = fields[0]
            field2 = fields[1]
            sign_fields[i] = (field1, field2)
        else:
            sign_fields[i] = (fields[0], None)
    base_string = "|"
    values = []
    for field1, field2 in sign_fields:
        if field2:
            values.append(str(payment.get(field1).get(field2)))
        else:
            values.append(str(payment.get(field1)))
    string = base_string.join(values)
    key = hmac.new(webhook_key, string.encode("utf-8"), hashlib.sha256).hexdigest()

    status = key == hash_key

    if not status:
        logging.warning(f'Платёж не прошел проверку. txnId: {payment.get("txnId")}')

    return status


if __name__ == "__main__":
    check_qiwi_payload()
