from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Balance, User, TelegramAuthToken


@receiver(post_save, sender=User)
def initialize_user_handler(sender, instance: User, **kwargs):
    """
    Автоматически создает Баланс для пользователя
    """
    # Если у пользователя нет баланса
    if not hasattr(instance, "balance"):
        Balance.objects.create(user=instance)

    if not hasattr(instance, "telegram_auth_token"):
        token = TelegramAuthToken.objects.create(user=instance)
        token.save()
