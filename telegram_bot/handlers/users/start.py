from os import remove as remove_file

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ICONS_MEDIA_URL
from data.texts import HELLO_STICKER_ID, START_NEW_USER, START_OLD_USER
from handlers.users.main_menu import main_menu_handler
from loader import bot, core, dp
from utils.exceptions import UserIsRegistered


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state=None):
    # Запрос на регистрацию пользователя
    mentor, coupon = await parse_start_args(message.get_args())
    if coupon:
        coupon = await core.pick_coupon(
            chat_id=message.from_user.id, coupon_code=coupon
        )
        await message.answer(f"Купон применен! {coupon.name}")
        return
    if state:
        await state.finish()
    photos = await bot.get_user_profile_photos(user_id=message.from_user.id, limit=1)
    user_photo = (
        await photos.photos[0][-1].download(ICONS_MEDIA_URL, make_dirs=True)
        if len(photos.photos) > 0
        else None
    )
    try:
        user = await core.register_user(
            user_data=message.from_user,
            user_photo_path=user_photo.name if user_photo else None,
            mentor_chat_id=mentor,
        )
    except UserIsRegistered:
        user = None
    if user:
        text = START_NEW_USER.format(name=message.from_user.first_name)
    else:
        text = START_OLD_USER.format(name=message.from_user.first_name)
    await message.answer_sticker(HELLO_STICKER_ID)
    await main_menu_handler(
        message, state, pre_text=text + "\n", user=user, base_text=""
    )

    if user_photo:
        remove_file(user_photo.name)


async def parse_start_args(args) -> 'Tuple["mentor", "coupon"]':
    if args.startswith("coupon"):
        return (None, args.replace("coupon_", ""))
    else:
        return (args, None)
