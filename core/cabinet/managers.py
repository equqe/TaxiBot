import logging

from django.contrib.auth.models import UserManager
from django.contrib.gis.db.models import QuerySet
from django.utils import timezone

from .utils import get_random_string
from dispatcher.settings import IN_PROGRESS_STATUSES


class CustomUserManager(UserManager):
    """
    Обновленный Менеджер для класса пользователя
    """

    def make_username(self, template: str = None, counter=0) -> str:
        """
        Функция генерирует случайное имя пользователя на основе шаблона, проверяет его на наличие в БД и возвращает его
        """
        if not template:
            template = get_random_string()

        new_username = template

        while self.filter(username=new_username):
            new_username = template + str(counter)
            counter += 1
        logging.info("New unique username=%s" % new_username)
        return new_username


class UserQuerySet(QuerySet):
    def active(self):
        # Возвращает незаблокированных пользователей
        now = timezone.now()
        return self.exclude(ban_start_date__lt=now, ban_end_date__gt=now)

    def telegram_ids(self):
        return self.exclude(telegram_data__isnull=True).values_list(
            "telegram_data__chat_id", flat=True
        )

    def drivers(self):
        return self.filter(driver__isnull=False)

    def active_drivers(self):
        now = timezone.now()
        return self.drivers().filter(
            driver__work_days__start_date__lt=now, driver__work_days__end_date__gt=now
        )

    def inactive_drivers(self):
        now = timezone.now()
        return self.drivers().exclude(
            driver__work_days__start_date__lt=now, driver__work_days__end_date__gt=now
        )

    def with_active_ride(self):
        return self.drivers().filter(rides__status__in=IN_PROGRESS_STATUSES)

    def without_active_ride(self):
        return self.drivers().exclude(rides__status__in=IN_PROGRESS_STATUSES)

    def clients(self):
        return self.filter(driver__isnull=True)

    def by_usergroup(self, usergroup: str):
        if usergroup == 1:
            return self.all()

        elif usergroup == 2:
            return self.drivers()

        elif usergroup == 3:
            return self.clients()

        elif usergroup == 4:
            return self.filter(is_staff=True)


class BanQuerySet(QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(start_date__lt=now, end_date__gt=now)

    def get_active_ban(self):
        # Возвращает один активный бан
        return self.active().first()


class WorkDriverDayQuerySet(QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(start_date__lt=now, end_date__gt=now)
