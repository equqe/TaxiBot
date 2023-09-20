from django.conf import settings as config
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils import timezone

from .settings import (
    COUPON_TYPES,
    MAILING_STATUS_CHOICES,
    MAILING_WAITING,
    USER_GROUP_CHOICES,
)


# Create your models here.


class AbstractCoupon(models.Model):
    """
    Абстрактный класс для модели купона. Если поле code пустое, то купон нельзя получить через код
    """

    value = models.PositiveIntegerField(verbose_name="Количество бонусов/дней")
    name = models.CharField(max_length=150, verbose_name="Название купона")
    code = models.CharField(
        max_length=30,
        unique=True,
        help_text="Уникальный код для купона, например: SALE2021. Максимальное количество символов: 30",
    )
    type = models.CharField(
        max_length=20, verbose_name="Тип купона", choices=COUPON_TYPES
    )
    quantity = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Количество купонов"
    )
    start_date = models.DateTimeField(
        verbose_name="Дата начала",
        help_text="Дата, до которой нельзя будет получить купон",
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания",
        null=True,
        help_text="Дата, после которой нельзя будет получить купон",
    )
    is_disposable = models.BooleanField(
        default=False,
        verbose_name="Одноразовый ли купон",
        help_text="Если да, то купон можно получить только 1 раз. Если нет, то после использования, можно будет снова получить купон.",
    )

    def __str__(self):
        return f"{self.name} [{self.code}]"

    class Meta:
        abstract = True
        verbose_name = "Купон"
        verbose_name_plural = "Купоны"
        ordering = ("-start_date",)

    @property
    def is_active(self):
        time_now = timezone.now()
        return self.start_date < time_now < self.end_date


class Coupon(AbstractCoupon):
    """
    Класс купона
    """

    @property
    def is_active(self):
        time_now = timezone.now()
        if (self.start_date < time_now < self.end_date) != True:
            return False
        if self.quantity:
            if self.get_busied_count() >= self.quantity:
                return False
        return True

    def get_busied_count(self):
        # Возвращает количество занятых купонов
        return self.users.count() + self.used_users.count()

    def get_absolute_url(self):
        return reverse("cabinet:coupon_detail", args=[self.pk])

    def get_apply_url(self):
        return reverse("cabinet:apply_coupon", args=[self.pk])

    def get_telegram_url(self):
        return (
            "https://t.me/"
            + config.TELEGRAM_BOT_USERNAME
            + f"?start=coupon_{self.code}"
        )


class Message(models.Model):
    """
    Модель поста для рассылки
    """

    text = models.TextField(max_length=4096, verbose_name="Текст")
    disable_notification = models.BooleanField(
        default=False, verbose_name="Отключить уведомления у получателей"
    )

    photo = models.ImageField(blank=True, null=True, verbose_name="Фото")
    video = models.FileField(blank=True, null=True, verbose_name="Видео")
    url = models.URLField("Ссылка в инлайн-кнопке", blank=True, null=True)
    url_button_name = models.CharField(
        "Название инлайн-кнопки", max_length=32, blank=True, null=True
    )

    def __str__(self):
        return f"%s. %s..." % (self.pk, self.text[:30])

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-pk"]

    def get_absolute_url(self):
        return reverse("cabinet:message_detail", args=[self.pk])


class Mailing(models.Model):
    """
    Модель рассылки
    """

    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    mailing_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата и время рассылки",
        help_text="Если оставить это поле пустым, то рассылка начнётся сразу же после создания. Время по МСК!",
    )
    user_group = models.IntegerField(
        choices=USER_GROUP_CHOICES,
        verbose_name="Группа пользователей, которая получит сообщение",
    )
    status = models.SmallIntegerField(
        default=MAILING_WAITING, choices=MAILING_STATUS_CHOICES, verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status", "-mailing_date"]

    def get_absolute_url(self):
        return reverse("cabinet:mailing_detail", args=[self.pk])


class Raffle(models.Model):
    """
    Модель розыгрыша
    """

    name = models.CharField(max_length=256, verbose_name="Название розыгрыша")
    winner = models.ForeignKey(
        "cabinet.User",
        on_delete=models.CASCADE,
        verbose_name="Победитель",
        related_name="raffle_wins",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сообщение победителю",
    )
    date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата проведения розыгрыша"
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        verbose_name="Купон, который получит победитель",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Розыгрыш"
        verbose_name_plural = "Розыгрыши"
        ordering = ["-date"]

    def get_absolute_url(self):
        return reverse("cabinet:raffle_detail", args=[self.pk])


class Present(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.PROTECT, verbose_name="Сообщение с призом"
    )
    city = models.ForeignKey(
        "dispatcher.City",
        on_delete=models.PROTECT,
        related_name="presents",
        verbose_name="Город, в котором будет действовать подарок",
        help_text="Подарок будет выдаваться только клиентам, которые закончили поездку в данном городе.",
    )

    class Meta:
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"

    def get_absolute_url(self):
        return reverse("cabinet:present_detail_view", args=[self.pk])
