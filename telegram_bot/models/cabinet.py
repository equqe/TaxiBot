import datetime
from typing import ForwardRef, List, Optional

from data.config import BASE_URL, DEBUG
from data.texts import (
    BASE_BALANCE_TEXT,
    CAR_BASE_TEXT,
    DRIVER_BASE_TEXT,
    OFFLINE_DRIVER_STATUS,
    ONLINE_DRIVER_STATUS,
    STATUS_BASE_TEXT,
)
from pydantic import BaseModel, validator

from .utils import parse_json_date

Location = ForwardRef("Location")
Coupon = ForwardRef("Coupon")


class CarBrand(BaseModel):
    """
    Марка автомобиля
    """

    name: str


class Car(BaseModel):
    """
    Модель данных автомобиля водителя
    """

    brand: CarBrand
    number: str
    color: str

    def as_text(self):
        return CAR_BASE_TEXT.format(
            name=self.brand.name, number=self.number, color=self.color
        )


class Driver(BaseModel):
    """
    Модель данных водителя
    """

    car: Car
    created_at: datetime.datetime
    is_active: bool
    phone_number: str
    photo_url: str

    # @validator('created_at', pre=True)
    # def date_validator(cls, value):
    #     return parse_json_date(value)

    def status_as_text(self):
        return STATUS_BASE_TEXT.format(
            ONLINE_DRIVER_STATUS if self.is_active else OFFLINE_DRIVER_STATUS
        )

    def as_text(self):
        return DRIVER_BASE_TEXT.format(
            car=self.car.as_text(),
            status=self.status_as_text(),
            phone_number=f"<b>Телефон: </b> {self.phone_number}",
        )

    def get_photo_url(self):
        if not DEBUG:
            return self.photo_url
        else:
            return "https://s.auto.drom.ru/i24246/pubs/4483/78851/3532207.jpg"


class Balance(BaseModel):
    money: float
    bonuses: float
    free_days: int

    def __repr__(self):
        return f"<Balance {self.money} ({self.bonuses})>"

    def as_text(self):
        return BASE_BALANCE_TEXT.format(
            money=self.money, bonuses=self.bonuses, free_days=self.free_days
        )


class TelegramData(BaseModel):
    chat_id: int
    username: str = None
    registration_date: datetime.datetime
    photo: str = None

    # # Преобразовывает datetime в верный формат
    # @validator('registration_date', pre=True)
    # def date_validator(cls, value):
    #     return parse_json_date(value)

    @property
    def photo_url(self):
        return BASE_URL + self.photo


class User(BaseModel):
    id: int
    username: str
    first_name: str
    date_joined: datetime.datetime
    coupons: List[Coupon]
    used_coupons: List[int]
    balance: Balance
    telegram_data: TelegramData
    location: Location = None

    phone_number: str = None
    telegram_auth_token: str = None
    last_name: str = None
    driver: Driver = None

    password: str = None

    def as_text(self):
        return "<b>Имя: </b> %s" % self.first_name

    def __repr__(self):
        text = f"<User id={self.id} username={self.username!r} first_name={self.first_name!r} {self.balance}>"
        return text

    def __str__(self):
        return f"<User id={self.id}, is_driver={bool(self.driver)}>"

    # # Преобразовывает datetime в верный формат
    # @validator('date_joined', pre=True)
    # def date_validator(cls, value):
    #     return parse_json_date(value)

    def get_coupon(self, pk: int):
        for coupon in self.coupons:
            if coupon.pk == pk:
                return coupon

    def get_ride_discount_coupons(self):
        """
            Возвращает список купонов на поездку
        :return:
        """
        coupons = []
        for coupon in self.coupons:
            if coupon.is_ride_discount():
                coupons.append(coupon)

        return coupons

    def generate_referral_link(self, bot_username: str):
        return f"t.me/{bot_username}?start={self.telegram_data.chat_id}"


class Settings(BaseModel):
    out_line_cost: float
    hide_cabinet_button: bool


def initialize_driver(json_data: dict) -> Optional[Driver]:
    """
    Принимает json_data и возвращает объект данных о водителе
    """
    if not json_data:
        return None

    return Driver(
        car=Car.parse_obj(json_data.get("car")),
        created_at=parse_json_date(json_data.get("created_at")),
        is_active=json_data.get("is_active"),
        photo_url=json_data.get("photo_url"),
    )


def initialize_balance(json_data: dict) -> Balance:
    return Balance(money=json_data.get("money"), bonuses=json_data.get("bonuses"))


def initialize_telegram_data(json_data: dict) -> TelegramData:
    return TelegramData.parse_obj(json_data)


def initialize_user(json_data: dict) -> User:
    """
    Принимает json_data от CoreAPI, на основании нее возвращает объект пользователя
    """
    return User.parse_obj(json_data)


if __name__ != "__main__":
    from .dispatcher import Location
    from .referral import Coupon

    __noinspection_pycharm__ = (Location, Coupon)
    User.update_forward_refs()
