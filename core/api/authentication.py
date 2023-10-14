from typing import Literal

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class EnvironmentAuthenticatedUser(AnonymousUser):
    """
    Класс анонимного пользователя для аутентификации через токен из переменной вирт. окружения
    его нет в базе данных, но он может проходить аутентификацию.
    Объект можно улучшать, добавляя методы на проверку прав
    """

    _ignore_model_permissions = True

    @property
    def is_authenticated(self) -> Literal[True]:
        return True

    def has_perms(*args, **kwargs) -> Literal[True]:
        return True


class EnvironmentTokenAuthentication(BaseAuthentication):
    """
    Класс для аутентификации через токен из переменных виртуального окружения
    Для аутентификации через него нужно использовать `EnvToken` в заголовке Authorization
    """

    _keyword = "EnvToken"
    _user = EnvironmentAuthenticatedUser()

    def authenticate(self, request: Request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self._keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise AuthenticationFailed(
                _("'Invalid enviroment token header. No credentials provided.")
            )

        elif len(auth) > 2:
            raise AuthenticationFailed(
                _(
                    "Invalid enviroment token header. Token string should not contain spaces."
                )
            )

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed(
                _(
                    "Invalid token header. Token string should not contain invalid characters."
                )
            )

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token: str):
        if token == settings.ENVIROMENT_CORE_TOKEN:
        
            return (self._user, None)
        else:
            raise AuthenticationFailed()
