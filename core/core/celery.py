import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", broker="redis://:foobared@redis:6379/3")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Возможно исправит ошибку с дублированием задач
# app.conf.broker_transport_options = {
# 'fanout_prefix': True,
# 'fanout_patterns': True
# }


# Поставить настройки выше в параметр core/settings.py CELERY_BROKER_TRANSPORT_OPTIONS={}

# Также добавить visibility_timeout и countdown (возможно его нет и для каждой задачи нужно отдельно)
