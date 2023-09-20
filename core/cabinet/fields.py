from django.db.models import DecimalField, PositiveIntegerField


class MoneyField(DecimalField):
    """
    Модель для хранения баланса пользователя
    """

    def __init__(self, *args, **kwargs):
        if not kwargs.get("max_digits"):
            kwargs["max_digits"] = 10
        if not kwargs.get("decimal_places"):
            kwargs["decimal_places"] = 2
        if not kwargs.get("verbose_name"):
            kwargs["verbose_name"] = "Количество денег"
        if not kwargs.get("help_text"):
            kwargs["help_text"] = "Максимальное значение: 999999,99"
        if not kwargs.get("default"):
            kwargs["default"] = 0
        super().__init__(*args, **kwargs)


class BonusesField(PositiveIntegerField):
    """
    Модель для хранения количества бонусов
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["verbose_name"] = "Количество бонусов"
        super().__init__(*args, **kwargs)
