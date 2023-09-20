from api.qiwi import (
    decrypt_webhook_key,
    delete_webhook,
    get_active_webhook,
    get_webhook,
    get_webhook_key,
    set_webhook,
)
from data.config import QIWI_WEBHOOK_URL
from pyqiwi import Wallet as BaseWallet
from utils.misc.logging import logger


class Wallet(BaseWallet):
    webhook = None
    _webhook_key = None

    def set_webhook(self):
        self.webhook = set_webhook(self.token, QIWI_WEBHOOK_URL)
        self.get_webhook_key()
        logger.info("Qiwi Webhook connected")

    def get_webhook_key(self):
        self.webhook_key_base64 = get_webhook_key(
            self.token, self.webhook.get("hookId")
        ).get("key")

    @property
    def webhook_key(self):
        if not self._webhook_key:
            self._webhook_key = decrypt_webhook_key(self.webhook_key_base64)
        return self._webhook_key

    def delete_webhook(self):
        if self.webhook:
            delete_webhook(self.token, self.webhook.get("hookId"))
            logger.info("Qiwi Webhook deleted")
        else:
            webhook = get_active_webhook(token=self.token)
            if webhook.get("hookId"):
                delete_webhook(self.token, webhook.get("hookId"))
                logger.info("Qiwi Webhook deleted")

    def get_webhook(self):
        self.webhook = get_webhook(self.token)
        self.get_webhook_key()


class WalletMock:
    def __init__(self, *args, **kwargs):
        pass

    def set_webhook(self, *args, **kwargs):
        pass

    def delete_webhook(self, *args, **kwargs):
        pass
