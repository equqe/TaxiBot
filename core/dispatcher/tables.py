import django_tables2 as tables
from django.utils.safestring import mark_safe

from dispatcher.models import Order, City
from django_tables2.utils import A


class ModelActionsMixin(tables.Table):
    """
    Добавляет кнопки взаимодействия с моделью
    """

    clickable = {
        "td": {"data-href": lambda record: record.get_absolute_url, "clickable": ""}
    }
    actions = tables.TemplateColumn(
        "<a class='btn btn-pill btn-primary' href='#'>Открыть</a>",
        verbose_name="Действия",
        orderable=False,
        attrs=clickable,
        exclude_from_export=True,
    )


class DriverOrdersTable(ModelActionsMixin, tables.Table):
    export_formats = ["xlsx", "csv"]

    class Meta:
        model = Order
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        fields = (
            "address",
            "cost",
            "payment_method",
            "comment",
            "take_order_date",
            "end_date",
        )
        empty_text = "История заказов пуста"


class AdminOrdersTable(ModelActionsMixin, tables.Table):
    def render_client(self, record):
        return mark_safe(
            f'<a href="{record.client.get_absolute_url()}">{record.client.__str__()}</a>'
        )

    def render_driver(self, record):
        return mark_safe(
            f'<a href="{record.driver.get_absolute_url()}">{record.driver.__str__()}</a>'
        )

    class Meta:
        model = Order
        sequence = ("...", "actions")
        exclude = (
            "start_location",
            "end_location",
            "suitable_drivers",
            "start_driver_location",
            "pull_up_driver_location",
        )
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        empty_text = "История заказов пуста"


class CityTable(ModelActionsMixin, tables.Table):
    class Meta:
        model = City
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        sequence = ("...", "actions")
        empty_text = "В системе нет городов"


# Отключаем сортировку по комментарию
DriverOrdersTable.base_columns["comment"].orderable = False
