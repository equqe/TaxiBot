from rest_framework.exceptions import APIException


class CouponNotAvailable(APIException):
    default_code = 400
    default_detail = "The specified coupon is not available"
    default_code = "bad_coupon"


COUPON_HAS_ALREADY_BEEN_USED = "coupon_has_already_been_used"
COUPON_DOES_NOT_EXIST = "coupon_does_not_exist"
