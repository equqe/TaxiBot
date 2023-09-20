from decimal import Decimal

from django.utils import timezone

from cabinet.models import User
from referral.managers import get_cost_with_coupon
from .geolocator import get_distance_of_locations
from ..exceptions import (
    BadRequest,
    ORDER_HAS_DRIVER,
    DRIVER_ALREADY_PICK_THIS_ORDER,
    DRIVER_ALREADY_HAS_ORDER,
)
from ..managers import get_closest_drivers_by_location
from ..models import Order, Settings, Location
from ..settings import (
    DRIVERS_NOT_FOUND,
    ORDER_IS_CREATED,
    ACCEPTED,
    SEARCH_NEAREST_DRIVERS_RADIUS,
)


def create_order(
    client: User,
    start_location: Location,
    end_location: Location,
    payment_method: str,
    client_phone: str,
    address: "dispatcher.Address",
    finish_address: "dispatcher.Address",
    coupon=None,
    is_need_baby_chair=False,
    comment = None,
    entrance = None,
) -> Order:
    """
    Создает заказ, применяет купоны и ищет подходящих водителей
    :type start_location: dispatcher.Location
    :type end_location: dispatcher.Location
    :type city: dispatcher.City
    :type coupon: referral.Coupon
    """
    if coupon:
        coupon = client.coupons.get(id=coupon.id)

    cost, raw_cost = get_cost_of_order(
        start_location=start_location,
        end_location=end_location,
        city=address.city,
        coupon=coupon,
        is_need_baby_chair=is_need_baby_chair,
    )
    drivers = get_closest_drivers_by_location(
        user=client,
        location=start_location,
        baby_chair=is_need_baby_chair,
        radius=address.city.search_drivers_radius or SEARCH_NEAREST_DRIVERS_RADIUS,
    )
    # Создаем объект заказа
    order = Order.objects.create(
        client=client,
        start_location=start_location,
        end_location=end_location,
        payment_method=payment_method,
        client_phone=client_phone,
        raw_cost=raw_cost,
        cost=cost,
        coupon=coupon,
        address=address,
        finish_address=finish_address,
        is_need_baby_chair=is_need_baby_chair,
        comment=comment,
        entrance=entrance,
    )
    if not drivers:
        # Если водители не найдены
        order.status = DRIVERS_NOT_FOUND
    else:
        # Если водители найдены
        order.status = ORDER_IS_CREATED
        order.suitable_drivers.set(drivers)

    order.save()

    return order


def get_cost_of_order(
    start_location: "Location",
    end_location: "Location",
    city: "City",
    coupon: "Coupon" = None,
    is_need_baby_chair: bool = False,
) -> Decimal:

    """
        Считает стоимость поездки

    :param start_location:  Точка отправления
    :param end_location:    Точка прибытия
    :param city:            Город отправления
    :param coupon:          Применненый купон, должен быть проверен на принадлежность пользователю заранее
    :param additional_costs: Добавочные стоимости
    :return: Итоговая стоимость поездки и стоимость поездки без применения купона
    """

    # # Настройки приложения (интервал ночного тарифа)
    # settings = get_app_settings()
    # # Время сейчас
    # time_now = datetime.datetime.now(tz=city.timezone).time()
    # is_night_tariff = not settings.night_tariff_start > time_now > settings.night_tariff_end
    # # Надбавочные стоимости при ночном тарифе (за поездку и за детское кресло)
    # night_allowance_cost, night_allowance_baby_chair = city.get_night_allowances()

    settings = Settings.objects.last()
    time_now = timezone.localtime(timezone=city.timezone).time()

    is_night_tariff = not (
        settings.default_tariff_start < time_now < settings.default_tariff_end
    )
    print(
        f"Локальное время при заказе: {time_now}\nTimezone: {city.timezone}\nis_night_tariff: {is_night_tariff}"
    )
    raw_cost = get_cost_of_order_by_locations(
        start_location=start_location,
        end_location=end_location,
        cost_per_km=city.get_cost_per_km(),
    )
    # Минимальная стоимость поездки в данном городе
    minimal_cost = city.get_minimal_cost()

    if is_night_tariff:
        raw_cost += city.cost_per_km.night_allowance
        minimal_cost += city.cost_per_km.night_allowance

    # Стоимость детского кресла
    if is_need_baby_chair:

        raw_cost += city.get_baby_chair_cost()
        minimal_cost += city.get_baby_chair_cost()
        if is_night_tariff:
            raw_cost += city.cost_per_baby_chair.night_allowance
            minimal_cost += city.cost_per_baby_chair.night_allowance

    # Стоимость с применением купона
    cost = get_cost_with_coupon(raw_cost, coupon)

    return max(cost, minimal_cost), max(raw_cost, minimal_cost)


def get_cost_of_order_by_locations(
    start_location: "Location", end_location: "Location", cost_per_km: Decimal
) -> Decimal:
    """
    Считает стоимость поездки, зная начальную и конечную геопозицию, также стоимость за километр
    """
    distance = get_distance_of_locations(
        start_location=start_location, end_location=end_location
    )
    distance = Decimal(distance)
    cost = distance * cost_per_km
    cost = cost.quantize(1)
    # Проверка на минимальную стоимость
    print(f"{cost=}")
    return cost


def set_driver_to_order(order: Order, driver: User):
    """
    Проверяет можно ли водителю дать заказ и выдает его
    """

    if driver.rides.in_progress():
        raise BadRequest(detail=DRIVER_ALREADY_HAS_ORDER)

    if order.driver:
        if order.driver.pk == driver.pk:
            raise BadRequest(detail=DRIVER_ALREADY_PICK_THIS_ORDER)
        else:
            raise BadRequest(detail=ORDER_HAS_DRIVER)

    order.driver = driver
    order.status = ACCEPTED
    order.take_order_date = timezone.now()
    order.start_driver_location = driver.location
    order.save()
    return order
