from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import core
from utils.exceptions import UserNotFound, PermissionDenied

KEY_PREFIX = "authentication"


class AuthenticationMiddleware(BaseMiddleware):
    """
    Middleware для автоматического запроса на получения или создания пользователя
    Добавляет к Message поле user -> message.user
    Для настройки можно использовать декоратор get_or_create_user
    """

    def __init__(
        self, key_prefix=KEY_PREFIX, raise_exception=False, disabled=True, fields=[]
    ):
        self.key_prefix = key_prefix
        self.raise_exception = raise_exception
        self.disabled = disabled
        self.fields = fields
        self.kwargs = {}
        super(AuthenticationMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        # Берём handler, который обертывается в данный момент
        handler = current_handler.get()

        if handler:
            # Запрашиваем параметры, которые выставлены с помощью декоратора
            raise_exception = getattr(
                handler, f"{self.key_prefix}__raise_exception", self.raise_exception
            )
            disabled = getattr(handler, f"{self.key_prefix}__disabled", self.disabled)
            fields = getattr(handler, f"{self.key_prefix}__fields", self.fields)
            kwargs = getattr(handler, f"{self.key_prefix}__kwargs", self.kwargs)
        else:
            raise_exception = self.raise_exception
            disabled = self.disabled
            fields = self.fields
            kwargs = self.kwargs

        if disabled:
            # Если запрос пользователя отключен, то ничего не делаем и заканчиваем работу функции
            message.user = None
            return

        # Запрашиваем пользователя
        if not getattr(message, "user", None):
            user = await core.get_user_by_chat_id(
                chat_id=message.from_user.id, **kwargs
            )
            # Присваем значение к объекту сообщения
            message.user = user

        if not user and raise_exception:
            raise UserNotFound

        for field in fields:
            if not getattr(user, field, None):
                raise PermissionDenied


def authenticate(raise_exception=False, disabled=False, fields: list = [], **kwargs):
    """
        Декоратор для настройки GetOrCreateUserMiddleware
        :param kwargs: Данные параметры передаются в функцию запроса пользователя
    :return:
    """

    def decorator(func):
        # Присваем аттрибуты к функции
        setattr(func, f"{KEY_PREFIX}__raise_exception", raise_exception)
        setattr(func, f"{KEY_PREFIX}__disabled", disabled)
        setattr(func, f"{KEY_PREFIX}__fields", fields)
        setattr(func, f"{KEY_PREFIX}__kwargs", kwargs)
        return func

    return decorator
