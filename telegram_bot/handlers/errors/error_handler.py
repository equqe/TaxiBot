import logging

from aiogram.types import Update
from aiogram.utils.exceptions import (
    CantDemoteChatCreator,
    CantParseEntities,
    InvalidQueryID,
    MessageCantBeDeleted,
    MessageNotModified,
    MessageTextIsEmpty,
    MessageToDeleteNotFound,
    RetryAfter,
    TelegramAPIError,
    Unauthorized,
)

from loader import dp, bot
from utils.exceptions import OrderError, OrderCanceledByClient
from data.config import ADMINS


@dp.errors_handler()
async def errors_handler(update: Update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    elif isinstance(exception, MessageNotModified):
        logging.debug("Message is not modified")
        return True
    elif isinstance(exception, MessageCantBeDeleted):
        logging.debug("Message cant be deleted")
        return True

    elif isinstance(exception, MessageToDeleteNotFound):
        logging.debug("Message to delete not found")
        return True

    elif isinstance(exception, MessageTextIsEmpty):
        logging.debug("MessageTextIsEmpty")
        return True

    elif isinstance(exception, Unauthorized):
        logging.info(f"Unauthorized: {exception}")
        return True

    elif isinstance(exception, InvalidQueryID):
        logging.exception(f"InvalidQueryID: {exception} \nUpdate: {update}")
        return True

    elif isinstance(exception, TelegramAPIError):
        logging.exception(f"TelegramAPIError: {exception} \nUpdate: {update}")
        return True
    elif isinstance(exception, RetryAfter):
        logging.exception(f"RetryAfter: {exception} \nUpdate: {update}")
        return True
    elif isinstance(exception, CantParseEntities):
        logging.exception(f"CantParseEntities: {exception} \nUpdate: {update}")
        return True

    elif isinstance(exception, OrderCanceledByClient):
        await inform_user(update, exception.message_text)
        try:
            await update.callback_query.message.delete()
        except Exception as E:
            logging.info(f"Не удалось удалить сообщение с ошибкой: {E.args}")
        return True

    else:
        if hasattr(exception, "message_text"):
            exception_name = exception.__class__.__name__
            if exception.raise_exception:
                # Если нужно рэйзить ошибку
                logging.exception(
                    f"{exception_name}: {exception.detail} \nUpdate: {update}"
                )
            else:
                # Если нужно просто залоггировать
                logging.info(f"{exception_name}: {exception.detail} \nUpdate: {update}")
            await inform_user(update, exception.message_text)
            return True
        else:
            await inform_user(
                update,
                "Произошла неизвестная нам ошибка. Мы уже работаем над её устранением!",
            )
            logging.exception(
                f"!!!NotRegisteredException: Update: {update} \n{exception}"
            )
            await inform_admin(exception)
            return True


async def inform_user(update, message_text):
    if getattr(update, "message"):
        # Если это сообщение
        await update.message.answer(message_text + "\n\n/menu - открыть главное меню")
    elif getattr(update, "callback_query"):
        # Если это callback
        message_text += "\n\n/menu - открыть главное меню"
        await update.callback_query.answer(message_text, show_alert=True)


async def inform_admin(exception):
    for admin in ADMINS:
        await bot.send_message(admin, f"Неизвестная ошибка:\n\n<code>{exception}</code>")
