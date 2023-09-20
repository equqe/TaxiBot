import django_tables2 as tables
from cabinet.models import User
from dispatcher.tables import ModelActionsMixin
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<img src="{url}" class="fav" height="50px", width="50px" style="border-radius: 50%;">',
            url=value.url,
        )


class UsersListTable(ModelActionsMixin, tables.Table):

    telegram_data__photo = ImageColumn(exclude_from_export=True)
    telegram_data__chat_id = tables.Column(visible=False)
    mentor = tables.Column(exclude_from_export=True)

    def render_mentor(self, record):
        mentor = record.mentor
        return mark_safe(f'<a href="{mentor.get_absolute_url()}">{mentor}</a>')

    class Meta:
        model = User
        template_name = "cabinet/django_tables/bootstrap4-responsive.html"
        fields = (
            "telegram_data__photo",
            "id",
            "username",
            "first_name",
            "date_joined",
            "last_login",
            "mentor",
        )
