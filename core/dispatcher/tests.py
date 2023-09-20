# Create your tests here.


import datetime
import random

from cabinet.models import User, Driver, Car, CarBrand
from .managers import get_closest_drivers_by_location
from .models import Location
from .models import Order

CAR_BRANDS = ["Toyota", "Nissan", "Mercedes Benz", "BMW"]
CAR_COLORS = "Чёрный Белый Синий Серый Жёлтый Зелёный".split()


def create_random_car_number():
    numbers = tuple("123456789")
    chars = tuple("АВЕКМНОРСТУХ")

    return "{}{}{}{}{}{}".format(
        random.choice(chars),
        random.choice(numbers),
        random.choice(numbers),
        random.choice(numbers),
        random.choice(chars),
        random.choice(chars),
    )


def timeit(func):
    def decorator(*args, **kwargs):
        start_time = datetime.datetime.now()
        a = func(*args, **kwargs)
        end_time = datetime.datetime.now()

        delta = end_time - start_time
        print(f"[Time of {func.__name__}]: ", delta.total_seconds())

        return a

    return decorator


def check_get_city_name():
    from dispatcher.models import Location
    from dispatcher.managers import get_city_name_by_location

    location = Location(longitude=30.439568, latitude=60.0523)
    town = get_city_name_by_location(location=location)
    print(town)


@timeit
def update_user_locations_from_base_location(
    base_location: tuple = (60.052408, 30.4394)
):
    from random import uniform

    users = User.objects.all().select_related("location")
    for user in users:
        delta = uniform(-1.0, 1.0)
        latitude = base_location[0] + delta
        longitude = base_location[1] + delta
        if not user.location:
            user.location = Location.objects.serialize_init(
                {"latitude": latitude, "longitude": longitude}
            )
        else:
            user.location.set_location(latitude, longitude)

        user.save()


@timeit
def create_users():
    usernames = range(100, 10_000)
    users = [User(username=username, first_name=username) for username in usernames]

    for user in users:
        user.save()

    #


@timeit
def users_to_drivers(users: "QuerySet"):
    for user in users:
        car_brand = CarBrand.objects.create(name="Nissan")
        car_brand.save()
        car = Car.objects.create(
            brand=car_brand,
            number=create_random_car_number(),
            color=random.choice(CAR_COLORS),
        )
        car.save()
        driver = Driver.objects.create(
            car=car, baby_chair=True, phone_number="8-921-999-88-99"
        )
        user.balance.free_days = 14
        user.balance.save()
        driver.save()
        user.driver = driver
        user.save()


# from dispatcher.tests import get_closest_drivers
# get_closest_drivers(pk=2)
@timeit
def get_closest_drivers(pk, max_count=10, baby_chair=False):
    from dispatcher.managers import get_distance_of_locations

    user = User.objects.get(pk=pk)
    users = User.objects.filter(
        driver__isnull=False, driver__is_active=True, driver__baby_chair=baby_chair
    ).select_related("location", "driver")

    drivers = []
    for driver in users:
        driver.distance = get_distance_of_locations(
            user.location, driver.location, units="meters"
        )
        drivers.append(driver)

    drivers.sort(key=lambda x: x.distance)
    return drivers[:max_count]


# from dispatcher.tests import get_closest_drivers_by_postgis
# get_closest_drivers_by_postgis(pk=2)
@timeit
def get_closest_drivers_by_postgis(pk, max_count=10):
    from django.contrib.gis.db.models.functions import Distance
    from django.contrib.gis.measure import D

    user = User.objects.get(pk=pk)
    base_location = user.location.point
    # users = User.objects.select_related('location').filter(location__point__distance_lte=(base_location, D(m=10000))).annotate(
    #    distance = Distance('location__point', base_location)
    # )
    users = (
        User.objects.select_related("location")
        .filter(location__point__distance_lte=(base_location, D(m=2000)))
        .annotate(distance=Distance("location__point", base_location))
        .order_by("distance")
    )

    return users[:max_count]


def check_values(list1, list2) -> bool:
    if len(list1) != len(list2):
        return False

    for i in range(len(list1) - 1):
        if list1[i].pk != list2[i].pk:
            return False

    return True


# from dispatcher.tests import check_get_drivers
# check_get_drivers(max_count=3)
def check_get_drivers(pk=2, max_count=10, baby_chair=False):
    user = User.objects.get(pk=pk)
    users1 = get_closest_drivers(pk=pk, max_count=max_count, baby_chair=baby_chair)
    users2 = get_closest_drivers_by_location(
        user=user, max_count=max_count, baby_chair=baby_chair
    )

    print(">> Users1:")
    for count, user in enumerate(users1):
        if count >= max_count:
            break
        print(
            f"  [%s] pk=%s | distance=%s | is_driver=%s, baby_chair=%s"
            % (count, user.pk, user.distance, bool(user.driver), user.driver.baby_chair)
        )

    print(">> Users2:")
    for count, user in enumerate(users2):
        if count >= max_count:
            break
        print(
            f"  [%s] pk=%s | distance=%s | is_driver=%s, baby_chair=%s"
            % (count, user.pk, user.distance, bool(user.driver), user.driver.baby_chair)
        )

    print("Значение совпадают: ", check_values(users1, users2))


# from dispatcher.tests import test_order_create
# test_order_create()
@timeit
def test_order_create(pk=2, baby_chair=False):
    from .models import City
    from .serializers import OrderSerializer

    user = User.objects.get(pk=pk)

    start_location = Location.objects.serialize_init(
        {"latitude": 60.052408, "longitude": 30.4394}
    )
    end_location = Location.objects.serialize_init(
        {"latitude": 60.0, "longitude": 30.0}
    )
    city = City.objects.get_city_by_location(start_location)
    order = Order.objects.create_order(
        client=user,
        start_location=start_location,
        end_location=end_location,
        payment_method="test",
        client_phone="8-999-333-22-22",
        city=city,
        address="Измайловская 10",
    )
    print(OrderSerializer(order).data)
    print(order.get_status_display())


RIDES_LOCATIONS = (
    ((59.931053, 30.336587), (59.870349, 30.294989)),
    ((59.939949, 30.248295), (59.958671, 30.303403)),
    ((59.989771, 30.255985), (60.040564, 30.300748)),
    ((59.902093, 30.513503), (59.946570, 30.420059)),
)


def get_random_locations():
    """
        Get random start and end locations of ride from RIDES_LOCATIONS
    :return:
    """
    start_location, end_location = random.choice(RIDES_LOCATIONS)
    start_location = {"latitude": start_location[0], "longitude": start_location[1]}
    end_location = {"latitude": end_location[0], "longitude": end_location[1]}

    return Location.objects.serialize_init(
        start_location
    ), Location.objects.serialize_init(end_location)


@timeit
def initializeFakeDriverProfile(user):
    """
    Функция создает водителю разные заказы, рабочие дни и так далее
    """
    # !!! Устарела
    from dispatcher.utils.order import create_order
    from dispatcher.utils.geolocator import get_address_by_location
    from .settings import RIDE_IS_FINISHED
    from django.utils import timezone

    start_location, end_location = get_random_locations()
    address = get_address_by_location(start_location)
    order = create_order(
        # Get random user as client
        client=User.objects.exclude(user=user).order_by("?").first(),
        start_location=start_location,
        end_location=end_location,
        payment_method=random.choice(["card", "cash"]),
        client_phone="8-999-123-22-44",
        address=address,
        coupon=None,
        is_need_baby_chair=False,
    )

    order.driver = user
    order.status = RIDE_IS_FINISHED
    order.end_date = timezone.now()


if __name__ == "__main__":
    pass
