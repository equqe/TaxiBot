import asyncio
import logging
from typing import List

from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loader import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def message_to_chat_id(
    chat_id: int,
    text=None,
    video=None,
    photo=None,
    url=None,
    url_button_name=None,
    **message_kwargs,
):
    """
    Отправляет сообщение указаному чату
    """
    # TODO: Хотфикс: тут стоит зарефачить
    if (url and url_button_name) and "reply_markup" not in message_kwargs:
        reply_markup = InlineKeyboardMarkup(row_width=1)
        reply_markup.add(InlineKeyboardButton(url_button_name, url=url))
    else:
        if reply_markup := message_kwargs.get("reply_markup"):
            del message_kwargs["reply_markup"]
    try:
        if photo:
            return await bot.send_photo(
                chat_id=chat_id,
                caption=text,
                photo=photo,
                reply_markup=reply_markup,
                **message_kwargs,
            )
        elif video:
            return await bot.send_video(
                chat_id=chat_id,
                caption=text,
                video=video,
                reply_markup=reply_markup,
                **message_kwargs,
            )
        else:
            await bot.send_message(
                chat_id=chat_id, text=text, reply_markup=reply_markup, **message_kwargs
            )
    except ChatNotFound:
        logging.info(f"[MAILING] chat_id={chat_id} not found (ChatNotFound)")
    except BotBlocked:
        logging.info(f"[MAILING] chat_id={chat_id} blocked bot")
    except Exception as E:
        logging.warning(f"[MAILING] chat_id={chat_id} unregistered exception! {E.args}")


async def message_to_user_list(
    user_list: List[int],
    text=None,
    video=None,
    photo=None,
    url=None,
    url_button_name=None,
    **message_kwargs,
):
    """
    Делает рассылку нескольким пользователям
    """
    for chat_id in user_list:
        await message_to_chat_id(
            chat_id=chat_id,
            text=text,
            video=video,
            photo=photo,
            url=url,
            url_button_name=url_button_name,
            **message_kwargs,
        )
        await asyncio.sleep(0.05)
