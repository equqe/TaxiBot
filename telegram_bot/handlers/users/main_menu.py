from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from os import remove as remove_file

from aiogram import types
from data.config import ICONS_MEDIA_URL
from data.texts import HELLO_STICKER_ID, START_NEW_USER, START_OLD_USER
from handlers.users.main_menu import main_menu_handler
from loader import bot, core, dp
from utils.exceptions import UserIsRegistered

from data.buttons import ADD_PHONE_NUMBER
from data.texts import OPEN_MAIN_MENU, SEND_PHONE, WRONG_PHONE
from keyboards.default import main_menu_keyboard
from keyboards.default.request_data import request_data_keyboard
from loader import bot, core, dp
from data import texts as t_data
from middlewares.authentication import authenticate
from states.main_menu import UpdatePhoneNumber
from utils.phone_numbers import validate_phone_number


@dp.message_handler(Command("menu"), state="*")
async def main_menu_handler(
    message: types.Message,
    state: FSMContext = None,
    pre_text: str = "",
    post_text: str = "",
    base_text: str = ...,
    user=None,
    chat_id: int = None,
):
    if state:
        await state.finish()

    chat_id = chat_id or message.from_user.id
    user = await core.get_user_by_chat_id(chat_id=chat_id, extended=True)

    text = base_text if base_text != ... else OPEN_MAIN_MENU
    await bot.send_message(
        chat_id,
        pre_text + text + post_text,
        reply_markup=await main_menu_keyboard(user=user),
    )


@dp.message_handler(text=ADD_PHONE_NUMBER)
async def phone_number_handler(message: types.Message):
    await UpdatePhoneNumber.is_active.set()
    await message.answer(
        SEND_PHONE, reply_markup=await request_data_keyboard(buttons=["phone"])
    )


@dp.message_handler(
    state=UpdatePhoneNumber.is_active, content_types=types.ContentTypes.ANY
)
@authenticate()
async def update_phone_number_handler(message: types.Message, state: FSMContext):
    contact = message.contact
    if contact:
        phone_number = validate_phone_number(contact.phone_number)
    else:
        phone_number = validate_phone_number(message.text)

    if not phone_number:
        await message.answer(
            WRONG_PHONE, reply_markup=await request_data_keyboard(buttons=["phone"])
        )
        return

    await core.update_user(user_id=message.user.id, phone_number=phone_number)
    await main_menu_handler(
        message, state, pre_text="Номер телефона успешно обновлён!\n\n"
    )
    keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=t_data.I_DRIVER),
            KeyboardButton(text=t_data.I_CLIENT)
        ]
    ],
    resize_keyboard=True
)
    await message.answer(reply_markup=keyboard, text="Выберете кто вы")


async def auntificate_client(message: types.Message, state: FSMContext):
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
    await message.answer_sticker(t_data.HELLO_STICKER_ID)
    await main_menu_handler(
        message, state, pre_text=text + "\n", user=user, base_text=""
    )

    if user_photo:
        remove_file(user_photo.name)

@dp.message_handler(text=t_data.I_CLIENT, commands=['menu'])
async def handle_client_choice(message: types.Message, state=None):
    await auntificate_client(message, state)


async def parse_start_args(args) -> 'Tuple["mentor", "coupon"]':
    if args.startswith("coupon"):
        return (None, args.replace("coupon_", ""))
    else:
        return (args, None)



@dp.message_handler(text=t_data.I_DRIVER, commands=['menu'])
async def handle_driver_choice(message: types.Message, state=None):
    await auntificate_client(message, state)


