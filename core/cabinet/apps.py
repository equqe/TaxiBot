from django.apps import AppConfig


class CabinetConfig(AppConfig):
    name = "cabinet"
    verbose_name = "Кабинет"

    def ready(self):
        """
        Вызывается при инициализации приложения, используется для избегания циркулярных импортов
        """
        from . import signals

        __noinspection__ = (signals,)
