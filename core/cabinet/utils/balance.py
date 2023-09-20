from decimal import Decimal
from typing import Union

from django.db.models import F

from cabinet.models import Balance


def update_user_balance(user_id: int, value: Union[Decimal, int, float], field: str):
    """
    Низкоуровневая функция для обновления баланса пользователя
    """
    balance = Balance.objects.filter(user__pk=user_id)
    if field == "money":
        balance.update(money=F("money") + value)
    elif field == "bonuses":
        balance.update(bonuses=F("bonuses") + value)
    elif field == "free_days":
        balance.update(free_days=F("free_days") + value)
