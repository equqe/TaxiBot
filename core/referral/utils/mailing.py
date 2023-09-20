from django.utils import timezone

from ..tasks import start_mailing


def initialize_mailing(mailing):
    """
    Принимает объект рассылки и обрабатывает его, добавляет в очередь или начинает рассылку лично
    """

    if not mailing.mailing_date:
        # Если время не указано, то начинаем рассылку прямо сейчас и ставим время
        mailing.mailing_date = timezone.now()
        mailing.save()
        start_mailing.apply_async((mailing.pk,))
