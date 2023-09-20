from ..models import Settings


def get_app_settings():
    return Settings.objects.last()
