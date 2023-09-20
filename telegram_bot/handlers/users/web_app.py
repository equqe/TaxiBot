import json
from typing import Any

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import core, dp
from middlewares.authentication import authenticate
from models.dispatcher import initialize_location


@dp.message_handler(state="*", content_types=types.ContentTypes.WEB_APP_DATA)
@authenticate()
async def web_app_test(message: types.Message, state: FSMContext):
    from .order import send_preorder

    data: dict[str, Any] = json.loads(message.web_app_data.data)
    order_data = {
        "start_location": initialize_location(data["start_location"]),
        "end_location": initialize_location(data["end_location"]),
        "is_need_baby_chair": data["baby_chair"],
        "client": message.user,
        "payment_method": data["payment_method"],
        "client_phone": message.user.phone_number,
        "comment": data.get("comment"),
        "coupon": data.get("coupon"),
        "entrance": data.get("entrance"),
    }

    order = await core.create_order(order_data)
    await send_preorder(message.from_user.id, order, state=state)
