import datetime
import logging

DATETIME_API_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def parse_json_date(date: str):
    """
    Парсит дату в формате str и возвращает datetime объект
    Иногда при случайности формат даты меняется, убирается Z, так как она равна 0, и происходит ValueError
    """
    # TODO: Убрать, уже не нужна
    return datetime.datetime.strptime(date, DATETIME_API_FORMAT)
