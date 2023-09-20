# Create your tests here.
from .models import TelegramData, User


def add_random_telegram_data_for_users(users):
    for user in users:
        tg = TelegramData(user=user, chat_id=user.id, username=None, photo=None)
        tg.save()


def add_telegram_data_to_drivers():
    drivers = User.objects.exclude(driver=None)
    add_random_telegram_data_for_users(drivers)


def translate_permission_names():
    from django.contrib.auth.models import Permission
    from .settings import DISPLAY_NAMES_OF_PERMISSIONS

    for codename, name in DISPLAY_NAMES_OF_PERMISSIONS:
        try:
            permission = Permission.objects.get(codename=codename)
            permission.name = name
            permission.save()
        except Permission.DoesNotExist:
            print(codename, " не обноружено")
