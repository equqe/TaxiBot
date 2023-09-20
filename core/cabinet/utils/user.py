from rest_framework.exceptions import ParseError

from cabinet.exceptions import NO_TELEGRAM_DATA, USER_IS_BLOCKED, USER_NOT_REGISTERED
from cabinet.models import User


def get_user_by_chat_id(chat_id):
    """
        Возвращает пользователя по chat_id или выдает ошибку
    :param chat_id:
    :return:
    """
    if not chat_id:
        raise ParseError(USER_NOT_REGISTERED.code)
    try:
        user = User.objects.get(telegram_data__chat_id=chat_id)
        if user.bans.active():
            raise ParseError(USER_IS_BLOCKED.code)

    except User.DoesNotExist:
        raise ParseError(detail=NO_TELEGRAM_DATA.code)

    return user
