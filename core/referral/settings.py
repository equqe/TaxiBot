COUPON_BONUS_TYPE = "bonuses"
COUPON_DISCOUNT_TYPE = "discount"
COUPON_FREE_DAYS_DRIVER_TYPE = "free_days_driver"

COUPON_TYPES = (
    (COUPON_BONUS_TYPE, "Купон на бонусы"),
    (COUPON_DISCOUNT_TYPE, "Купон на скидку на поездку"),
    (COUPON_FREE_DAYS_DRIVER_TYPE, "Купон на пробный период"),
)


USER_GROUP_CHOICES = (
    (1, "Все пользователи"),
    (2, "Водители"),
    (3, "Клиенты"),
    (4, "Администраторы"),
)


MAILING_WAITING = 1
MAILING_STARTED = 2
MAILING_FINISHED = 3

MAILING_STATUS_CHOICES = (
    (MAILING_WAITING, "Ожидается"),
    (MAILING_STARTED, "Рассылка началась"),
    (MAILING_FINISHED, "Рассылка окончена"),
)
