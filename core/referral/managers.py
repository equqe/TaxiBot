from decimal import Decimal

from .exceptions import CouponNotAvailable


def check_coupon(coupon: "Coupon") -> bool:
    """
    Проверяет подходит ли купон для скидки на поездку
    """
    if coupon:
        if coupon.type == "discount":
            return True
        else:
            raise CouponNotAvailable('Coupon must be a "discount" type')

    return False


def get_cost_with_coupon(cost: Decimal, coupon: "Coupon") -> float:
    if check_coupon(coupon):
        cost -= coupon.value

    return cost
