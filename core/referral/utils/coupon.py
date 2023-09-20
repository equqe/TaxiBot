from cabinet.models import User
from referral.models import Coupon
from rest_framework.exceptions import ParseError

from ..exceptions import COUPON_HAS_ALREADY_BEEN_USED
from ..settings import (
    COUPON_FREE_DAYS_DRIVER_TYPE,
    COUPON_BONUS_TYPE,
    COUPON_DISCOUNT_TYPE,
)
from cabinet.utils.balance import update_user_balance


def give_coupon_to_user(user: User, coupon: Coupon):
    """
    Функция выдает купон пользователю
    """
    if coupon.is_disposable and (
        coupon in user.used_coupons.all() or coupon in user.coupons.all()
    ):
        # Если купон одноразовый и пользователь уже использовал его когда-то
        raise ParseError(COUPON_HAS_ALREADY_BEEN_USED)

    if not coupon.is_active:
        # Если купон неактивен
        raise ParseError("bad_coupon")

    user.coupons.add(coupon.pk)
    user.save()
    return user


def apply_coupon(user: User, coupon: Coupon):
    """
    Применяет купон
    """
    status = False
    if coupon.type == COUPON_FREE_DAYS_DRIVER_TYPE:
        update_user_balance(user_id=user.pk, value=coupon.value, field="free_days")
        status = True
    elif coupon.type == COUPON_BONUS_TYPE:
        update_user_balance(user_id=user.pk, value=coupon.value, field="bonuses")
        status = True

    if status:
        user.used_coupons.add(coupon.pk)
        user.coupons.remove(coupon.pk)
    return status
