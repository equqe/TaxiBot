import datetime
from typing import List, ForwardRef, Union

from data.texts import COUPON_BASE_TEXT
from pydantic import BaseModel, validator

from .utils import parse_json_date

RIDE_DISCOUNT_TYPE = "discount"

City = ForwardRef("City")


class Coupon(BaseModel):
    id: int
    value: int
    name: str
    code: str = None
    type: str
    quantity: int = None
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None

    # # Преобразовывает datetime в верный формат
    # @validator('start_date', 'end_date', pre=True)
    # def date_validator(cls, value):
    # 	return parse_json_date(value)

    def as_text(self) -> str:
        return COUPON_BASE_TEXT.format(
            coupon_info=self.name, coupon_discount=self.value
        )

    def is_ride_discount(self):
        return self.type == RIDE_DISCOUNT_TYPE


class Message(BaseModel):
    text: str
    disable_notification: bool

    photo_url: str = None
    video_url: str = None
    url: str = None
    url_button_name: str = None

    def get_message_kwargs(self):
        return {"disable_notification": self.disable_notification}

    async def send(self, chat_id: int):
        from utils.mailing import message_to_chat_id

        await message_to_chat_id(
            chat_id=chat_id,
            text=self.text,
            photo=self.photo_url,
            video=self.video_url,
            **self.get_message_kwargs()
        )


class Mailing(BaseModel):
    message: Message
    telegram_ids: List[int]

    async def start(self):
        from utils.mailing import message_to_user_list

        await message_to_user_list(
            user_list=self.telegram_ids,
            text=self.message.text,
            photo=self.message.photo_url,
            video=self.message.video_url,
            **self.message.get_message_kwargs()
        )


class Present(BaseModel):
    message: Message
    city: City


def initialize_coupon(json_data: dict) -> Coupon:
    """
    Создает объект купона и возвращает его
    """
    if not json_data:
        return None

    coupon = Coupon(
        id=int(json_data.get("id")),
        value=json_data.get("value"),
        name=json_data.get("name"),
        code=json_data.get("code"),
        type=json_data.get("type"),
        quantity=json_data.get("quantity"),
        start_date=json_data.get("start_date"),
        end_date=json_data.get("end_date"),
    )

    return coupon


async def initialize_present(json_data: dict) -> Union[Present, None]:
    print(json_data)
    if json_data:
        return Present.parse_obj(json_data)
    else:
        return None


if __name__ != "__main__":
    from .dispatcher import City

    __no_inspection_pycharm = (City,)
    Present.update_forward_refs()
