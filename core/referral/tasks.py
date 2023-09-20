import datetime

import requests
from cabinet.models import Settings as CabinetSettings
from cabinet.models import User
from celery.schedules import crontab
from core import celery_app
from django.conf import settings as config
from django.utils import timezone

from .models import Mailing
from .serializers import MailingSerializer, MessageSerializer
from .settings import MAILING_FINISHED, MAILING_STARTED, MAILING_WAITING


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender: celery_app, **kwargs):
    # Устанавливает регулярные задачи
    print("setup_periodic_tasks()")
    sender.add_periodic_task(crontab(hour=10), remind_notify.s())
    sender.add_periodic_task(50.0, check_mailings.s())


@celery_app.task
def start_mailing(mailing_pk: int):
    mailing = Mailing.objects.get(pk=mailing_pk)
    if mailing.status != MAILING_WAITING:
        print("Рассылка уже началась, а это дубликат!")
        return None
    print(f"Рассылка #{mailing.pk} началась, {mailing.mailing_date=}.")
    mailing.status = MAILING_STARTED
    mailing.save()
    # Рассылка
    print(MailingSerializer(mailing).data)
    send_mailing_to_bot(data=MailingSerializer(mailing).data)

    mailing.status = MAILING_FINISHED
    mailing.save()
    print(f"Рассылка #{mailing.pk} завершена, {timezone.now()=}")


@celery_app.task
def check_mailings():
    print("Проверка рассылок")
    now = timezone.now()
    mailings = Mailing.objects.filter(mailing_date__lte=now, status=MAILING_WAITING)
    for mailing in mailings:
        start_mailing.apply_async((mailing.pk,))


@celery_app.task
def remind_notify():
    # Отправляет определенное сообщение всем пользователям, которые не делали заказа 5 дней
    start_datetime = timezone.now() - datetime.timedelta(days=5)
    # Берем всех пользователей, уведомления которым приходили больше чем 5 дней назад
    users = User.objects.filter(last_message_1_datetime__lte=start_datetime)
    print(users.count())
    # Обновляем дату последнего обновления на нынешнюю
    users.update(last_message_1_datetime=timezone.now())
    # Берем сообщение, которое нужно отправлять пользователям в данном случае
    message = CabinetSettings.objects.last().message_1
    # Делаем сырую рассылку
    send_mailing_to_bot(
        data={
            "message": MessageSerializer(message).data,
            "telegram_ids": list(users.telegram_ids()),
        }
    )


def send_mailing_to_bot(data: dict):
    print(f"{config.TELEGRAM_BOT_WEBHOOK_URL=}")
    telegram_bot_response = requests.post(
        config.TELEGRAM_BOT_WEBHOOK_URL + "mailing/",
        json=data,
        headers={"Content-Type": "application/json"},
    )
