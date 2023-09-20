from rest_framework.exceptions import APIException


class CityNotFound(APIException):
    """
    Город не обслуживается
    """

    status_code = 416  # Диапазон не достижим
    default_detail = "city_not_found"
    default_code = "city_not_found"


class BadRequest(APIException):
    """
    Неверный запрос
    """

    status_code = 400
    default_detail = "bad_request"
    default_code = "bad_request"


DRIVER_ALREADY_HAS_ORDER = "driver_already_has_order"
ORDER_HAS_DRIVER = "order_has_driver"
DRIVER_ALREADY_PICK_THIS_ORDER = "this_driver_already_pick_this_order"
CLIENT_ALREADY_HAS_ORDER = "client_already_has_order"

NOT_VALID_STATUS = "not_valid_order_status"

USER_DONT_HAVE_ORDER = "no_order"
ORDER_CANCELED_BY_CLIENT_ERROR = "order_canceled_by_client"
