import datetime
from typing import ForwardRef, List

from data.buttons import PAYMENT_METHOD_CARD, PAYMENT_METHOD_CASH, ORDER_A_TAXI
from data.texts import COMMENT_BASE_TEXT, ORDER_BASE_TEXT, PRICE_BASE_TEXT
from pydantic import BaseModel

User = ForwardRef("User")
Coupon = ForwardRef("Coupon")

PAYMENT_METHOD_CHOICES = {PAYMENT_METHOD_CASH: "cash", PAYMENT_METHOD_CARD: "card"}

# Четвертая сотня выделена под ошибки
DRIVERS_NOT_FOUND = 401
NO_ACCEPT_BY_DRIVERS = 402
RIDE_IS_FINISHED_WITHOUT_PAYMENT = 403
ORDER_CANCELED_BY_CLIENT = 404
ORDER_CANCELED_BY_DRIVER = 405

# Первая сотня выделена под успешные статусы
ORDER_IS_CREATED = 100
WAIT_TO_ACCEPT = 101
ACCEPTED = 102
DRIVER_IS_WAITING = 103
RIDE_IS_STARTED = 104
RIDE_IS_FINISHED = 105

ORDER_STATUSES = {
    ORDER_IS_CREATED: "Заказ создан",
    DRIVERS_NOT_FOUND: "Не обнаружено водителей по-близости",
    WAIT_TO_ACCEPT: "Ожидается принятие заказа одним из водителей",
    NO_ACCEPT_BY_DRIVERS: "Ни один из водителей не принял заказ",
    ACCEPTED: "Заказ принят водителем",
    DRIVER_IS_WAITING: "Водитель подъехал и ожидает клиента",
    RIDE_IS_STARTED: "Клиент сел в машину к водителю",
    RIDE_IS_FINISHED_WITHOUT_PAYMENT: "Водитель ожидает оплату за поездку",
    RIDE_IS_FINISHED: "Поездка завершена",
    ORDER_CANCELED_BY_CLIENT: "Поездка отменена клиентом",
    ORDER_CANCELED_BY_DRIVER: "Поездка отменена водителем",
}


class Location(BaseModel):
    """
    Класс для хранения геопозиции
    """

    latitude: float
    longitude: float

    def __repr__(self):
        return "<Location: %s %s >" % self.as_tuple()

    def as_tuple(self) -> tuple:
        return (self.latitude, self.longitude)

    def as_dict(self) -> dict:
        return {"latitude": self.latitude, "longitude": self.longitude}


class City(BaseModel):
    id: int
    name: str
    # timezone: str


class Address(BaseModel):
    place_id: int
    city: City
    road: str = None
    house_number: str = None

    def __str__(self):
        return ", ".join(
            tuple(
                filter(
                    None,
                    (self.city.name, self.road, self.house_number),
                )
            )
        )


class OrderReview(BaseModel):
    stars: int
    text: str = None


class Order(BaseModel):
    id: int
    client: User
    driver: User = None
    start_location: Location
    end_location: Location
    raw_cost: float
    cost: float
    address: Address
    finish_address: Address = None
    payment_method: str
    client_phone: str
    status: int
    is_need_baby_chair: bool
    coupon: Coupon = None
    suitable_drivers: List[User] = None
    comment: str = None
    review: OrderReview = None
    entrance: str = None

    def as_text(self, for_driver=False) -> str:
        """
        Возвращает строку описания заказа для сообщения
        """
        entrance = ""
        if self.entrance:
            entrance = f", подъезд {self.entrance}"
        return ORDER_BASE_TEXT.format(
            address=str(self.address) + entrance,
            finish_address=self.finish_address or "Будет указан в геопозиции",
            info=self.get_info(for_driver=for_driver),
        )

    def get_info(self, for_driver=False) -> str:
        text = self.get_price_as_text()

        if self.coupon and not for_driver:
            # Купон ненужно показывать водителю
            text += f"\n{self.coupon.as_text()}"

        text += f"\n<b>Способ оплаты: </b>{self.get_payment_method_as_text()}"
        # text += f'\n<b>Статус:</b> {ORDER_STATUSES.get(self.status)}'

        if self.comment:
            text += "\n" + COMMENT_BASE_TEXT.format(self.comment)

        if self.driver and not for_driver:
            text += "\n\n<u>Данные водителя</u>"
            text += "\n" + f"<b>Имя: </b> {self.driver.first_name}"
            text += "\n" + self.driver.driver.as_text()

        if for_driver:
            text += "\n<u>Данные клиента</u>"
            text += f"\n{self.client.as_text()}"

            if self.status == RIDE_IS_FINISHED:
                text += "\n\n" + self.get_price_as_text()

        if not for_driver and self.status == ORDER_IS_CREATED:
            text += (
                "\n\n"
                + f"⚠️ Нажмите кнопку ниже «{ORDER_A_TAXI}», чтобы я принял ваш заказ!"
            )

        if self.status > WAIT_TO_ACCEPT:
            text += "\n\n"
            if for_driver:
                text += "⚠️ Вы можете отправить любое сообщение мне и я его перешлю клиенту, который заказал такси. Я, так же, буду присылать вам сообщения, которые отправил клиент!"
            else:
                text += "⚠️ Вы можете отправить любое сообщение мне и я его перешлю водителю, который принял ваш заказ. Я, так же, буду присылать вам сообщения, которые отправил водитель!"

        return text

    def get_price_as_text(self) -> str:
        price_info = f"{self.cost:.0f} руб."
        if self.cost < self.raw_cost:
            price_info += f" <strike>{self.raw_cost:.0f} руб.</strike>"
        return PRICE_BASE_TEXT.format(price_info=price_info)

    def get_payment_method_as_text(self) -> str:
        for text, code in PAYMENT_METHOD_CHOICES.items():
            if code == self.payment_method:
                return text

    def get_address_text(self):
        return ",".join(
            *(self.address.city.name, self.address.road, self.address.house_number, self.entrance)
        )

    def get_driver_photo(self):
        return self.driver.driver.get_photo_url()


class Settings(BaseModel):
    default_tariff_start: datetime.time
    default_tariff_end: datetime.time
    waiting_free_minutes: int
    waiting_price: float


def initialize_location(json_data: dict) -> Location:
    return Location.parse_obj(json_data)


def initialize_city(json_data: dict) -> City:
    return City.parse_obj(json_data)


def initialize_order(json_data) -> Order:
    print("initialize order: ", json_data)
    return Order.parse_obj(json_data)


if __name__ != "__main__":
    from .cabinet import User
    from .referral import Coupon

    # Обновляет зависимости, используется, чтобы избежать циркулярных импортов
    __noinspection_pycharm__ = (User, Coupon)
    Order.update_forward_refs()
