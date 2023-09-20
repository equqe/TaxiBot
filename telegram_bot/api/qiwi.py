import base64

from pyqiwi.apihelper import _make_request


def set_webhook(token: str, url: str):
    result = _make_request(
        token=token,
        method_name=f"payment-notifier/v1/hooks?hookType=1&param={url}&txnType=0",
        method="put",
    )
    return result


def get_active_webhook(token: str):
    result = _make_request(
        token=token, method_name=f"/payment-notifier/v1/hooks/active", method="get"
    )
    return result


def delete_webhook(token: str, hook_id: str):
    result = _make_request(
        token=token, method_name=f"payment-notifier/v1/hooks/{hook_id}", method="delete"
    )
    return result


def get_webhook(token: str):
    result = _make_request(
        token=token, method_name=f"/payment-notifier/v1/hooks/active", method="get"
    )
    return result


def get_webhook_key(token, hook_id):
    result = _make_request(
        token=token,
        method_name=f"/payment-notifier/v1/hooks/{hook_id}/key",
        method="get",
    )
    return result


def decrypt_webhook_key(webhook_key_base64):
    return base64.b64decode(bytes(webhook_key_base64, "utf-8"))
