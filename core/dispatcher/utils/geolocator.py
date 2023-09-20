import logging
from time import sleep

import geopy.distance
import requests
from dadata import Dadata
from django.conf import settings as config
from geopy.geocoders import Nominatim

from ..exceptions import BadRequest, CityNotFound
from ..models import Address, City, Location

dadata = Dadata(config.DADATA_TOKEN)
DADATA_GEOLOCATOR_PARAMS = {"count": 1}


def get_distance_of_locations(
    start_location: Location, end_location: Location, units="km"
) -> float:
    """
    Считает расстояние между двумя координатами, значение возвращает в километрах
    """
    try:
        start_tuple: tuple = start_location.as_tuple()
        end_tuple: tuple = end_location.as_tuple()
        start = f"{start_tuple[1]},{start_tuple[0]}"
        end = f"{end_tuple[1]},{end_tuple[0]}"
        routing_response = requests.get(
            url=f"http://188.68.204.75:5000/route/v1/driving/{start};{end}?steps=false"
        )
        data: dict = routing_response.json()
        if data.get("code") != "Ok":
            raise Exception

        distance = geopy.distance.Distance(meters=data["routes"][0]["distance"])

    except Exception as E:
        logging.warning(E.args)
        distance = geopy.distance.great_circle(
            start_location.as_tuple(), end_location.as_tuple()
        )

    if units == "meters":
        distance = distance.meters
    else:
        distance = distance.km

    return distance


def get_raw_geolocation_data_by_location(location: Location):
    """
    Возвращает данные о местоположении
    """

    result = dadata.geolocate(
        "address", *location.as_tuple(), **DADATA_GEOLOCATOR_PARAMS
    )
    if result:
        data = result[0]
    else:
        data = None

    return data["data"]


def get_city_name_by_location(location: Location) -> str:
    """
    Возвращает название города по координатам
    """
    data = get_raw_geolocation_data_by_location(location=location)
    address = data.get("address")
    city = address.get("city") or address.get("town") or address.get("settlement")

    if not city:
        raise CityNotFound

    return city


def get_address_by_location(location: Location) -> Address:
    """
    Создает или запрашивает модель адреса по координатам
    """
    data, retry_count = (None, 0)

    # Геолокатор иногда обрывает соединение, так будет несколько попыток раз в 2 секунды
    while not data and retry_count < 3:
        try:
            data = get_raw_geolocation_data_by_location(location=location)
        except Exception as E:
            logging.warning(f"Exception in get_address_by_location:\n{E}")
            sleep(2)
        retry_count += 1
    # Если геолокатор так и не ответил или не обнаружил местоположение поднимаем ошибку
    if not data:
        raise CityNotFound

    # Получаем уникальный идентификатор города в БД Nominatim
    place_id = int(data["kladr_id"])

    # Получаем название города, иногда она хранится в `city`, иногда в `town`
    city_name = data.get("settlement") or data.get("city")

    # Если название города не определено, то поднимаем ошибку
    if not city_name:
        raise CityNotFound
    # Запрашиваем город из БД
    city = City.objects.get_city_by_name(name=city_name)
    # Запрашиваем или создаем адрес
    address, is_created = Address.objects.get_or_create(
        city=city, road=data.get("street"), house_number=data.get("house")
    )
    if is_created:
        address.save()

    return address
