from decimal import Decimal

# Количество звёзд, при котором заказ считается плохим.
# В данном случае, все заказы, в которых кол-во звёзд меньше или равно двум - плохие
BAD_ORDER_STARS = 2
STARS_TYPES = (
    (1, "⭐"),
    (2, "⭐" * 2),
    (3, "⭐" * 3),
    (4, "⭐" * 4),
    (5, "⭐" * 5),
)

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


ORDER_STATUSES = (
    (ORDER_IS_CREATED, "Заказ создан"),
    (DRIVERS_NOT_FOUND, "Не обнаружено водителей по-близости"),
    (WAIT_TO_ACCEPT, "Ожидается принятие заказа одним из водителей"),
    (NO_ACCEPT_BY_DRIVERS, "Ни один из водителей не принял заказ"),
    (ACCEPTED, "Заказ принят водителем"),
    (DRIVER_IS_WAITING, "Водитель подъехал и ожидает клиента"),
    (RIDE_IS_STARTED, "Клиент сел в машину к водителю"),
    (RIDE_IS_FINISHED_WITHOUT_PAYMENT, "Водитель ожидает оплату за поездку"),
    (RIDE_IS_FINISHED, "Поездка завершена"),
    (ORDER_CANCELED_BY_CLIENT, "Заказ отменён клиентом"),
    (ORDER_CANCELED_BY_DRIVER, "Заказ отменён водителем"),
)

IN_PROGRESS_STATUSES = (
    ORDER_IS_CREATED,
    WAIT_TO_ACCEPT,
    ACCEPTED,
    DRIVER_IS_WAITING,
    RIDE_IS_STARTED,
)


TIMEZONE_CHOICES = [(i, f"GMT {i:+d}") for i in range(-12, 13)]

MINIMAL_COST_OF_RIDE = Decimal(50.0)
DEFAULT_BABY_CHAIR_COST = Decimal(30.0)

# Радиус поиска водителей в метрах
SEARCH_NEAREST_DRIVERS_RADIUS = 30000
