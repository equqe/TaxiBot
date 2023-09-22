from datetime import timedelta

import requests
from django.utils import timezone
from django.conf import settings as config
from core import celery_app
from .models import OrderRevision
from .settings import DRIVERS_NOT_FOUND, SEARCH_NEAREST_DRIVERS_RADIUS
from .managers import get_closest_drivers_by_location
from .serializers import OrderRevisionNotifySerializer


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender: celery_app, **kwargs):
    # Устанавливает регулярные задачи
    sender.add_periodic_task(30.0, check_revision_orders.s())


@celery_app.task
def check_revision_orders():
    # TODO: Убрать принты
    now = timezone.now()
    success_orders = []
    failed_orders = []
    to_update_revision_ids = []
    revisions = OrderRevision.objects.select_related(
        "order",
        "order__start_location",
        "order__client",
        "order__client__telegram_data",
        "order__address",
        "order__address__city",
    ).filter(order__status=DRIVERS_NOT_FOUND, end_date__gte=now, is_active=True)

    print(f"check_revision_orders >> {revisions=}")

    for revision in revisions:
        drivers = get_closest_drivers_by_location(
            user=revision.order.client,
            location=revision.order.start_location,
            baby_chair=revision.order.is_need_baby_chair,
            radius=revision.order.address.city.search_drivers_radius
            or SEARCH_NEAREST_DRIVERS_RADIUS,
        )

        if drivers:
            success_orders.append(revision.order)
            to_update_revision_ids.append(revision.pk)

        else:
            if revision.end_date - now < timedelta(minutes=1):
                failed_orders.append(revision.order)
                to_update_revision_ids.append(revision.pk)

    revisions.filter(pk__in=to_update_revision_ids).update(is_active=False)
    success = OrderRevisionNotifySerializer(success_orders, many=True).data
    failed = OrderRevisionNotifySerializer(failed_orders, many=True).data
    print(f"check_revision_orders >> {len(success)=} {len(failed)=}")
    if success or failed:
        telegram_bot_response = requests.post(
            config.TELEGRAM_BOT_WEBHOOK_URL + "orderRevisionNotify/",
            json={"success": success, "failed": failed},
            headers={"Content-Type": "application/json"},
        )

        print(f"{telegram_bot_response.status_code=}")
    else:
        print("check_revision_orders >> no data")
