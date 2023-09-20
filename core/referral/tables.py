import django_tables2
from dispatcher.tables import ModelActionsMixin
from django.utils.safestring import mark_safe

from .models import Coupon, Mailing, Message, Present, Raffle


class CouponsTable(ModelActionsMixin, django_tables2.Table):
    export_formats = ["xlsx"]

    class Meta:
        model = Coupon
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        fields = (
            "name",
            "code",
            "type",
            "value",
            "quantity",
            "start_date",
            "end_date",
            "is_disposable",
        )
        empty_text = "Нет купонов"


class CouponsDriverTable(django_tables2.Table):
    clickable = {
        "td": {"data-href": lambda record: record.get_apply_url, "clickable": ""}
    }
    actions = django_tables2.TemplateColumn(
        "<a class='btn btn-pill btn-primary' href='#'>Применить</a>",
        verbose_name="Действия",
        orderable=False,
        attrs=clickable,
        exclude_from_export=True,
    )

    class Meta(CouponsTable.Meta):
        model = Coupon
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        empty_text = "Нет купонов"
        fields = ("name", "type", "value", "actions")


class MessageTable(ModelActionsMixin, django_tables2.Table):
    class Meta:
        model = Message
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        sequence = ("...", "actions")
        empty_text = "Нет сообщений"


class MailingTable(ModelActionsMixin, django_tables2.Table):
    def render_message(self, record):
        return mark_safe(
            '<a href="%s">%s</a>' % (record.message.get_absolute_url(), record.message)
        )

    class Meta:
        model = Mailing
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        sequence = ("...", "actions")
        empty_text = "Нет рассылок"


class RaffleTable(ModelActionsMixin, django_tables2.Table):
    def render_winner(self, record):
        return mark_safe(
            '<a href="%s">%s</a>' % (record.winner.get_absolute_url(), record.winner)
        )

    def render_coupon(self, record):
        return mark_safe(
            '<a href="%s">%s</a>' % (record.coupon.get_absolute_url(), record.coupon)
        )

    class Meta:
        model = Raffle
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        sequence = ("...", "actions")
        empty_text = "Розыгрыши отсутствуют"


class PresentTable(ModelActionsMixin, django_tables2.Table):
    class Meta:
        model = Present
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        empty_text = "Подарки отсутствуют"
