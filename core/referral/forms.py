from cabinet.forms import LayoutMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Coupon, Mailing, Message, Raffle, Present


class CouponForm(LayoutMixin, forms.ModelForm):
    """
    Форма для редактирования пользователя в кабинете администратора
    """

    helper = FormHelper()
    helper.form_method = "post"
    helper.form_class = "theme-form"
    layout_header = "Основная информация о купоне"
    layout_buttons = [
        Submit("submit", "Сохранить", css_class="btn-primary"),
        Submit("delete", "Удалить", css_class="btn-secondary"),
    ]

    class Meta:
        model = Coupon
        fields = "__all__"


class CreateCouponForm(CouponForm):
    layout_header = "Создание нового купона"
    layout_buttons = [Submit("submit", "Создать новый купон", css_class="btn-primary")]


class MessageForm(LayoutMixin, forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Редактирование сообщения"
    layout_buttons = [
        Submit("submit", "Сохранить", css_class="btn-primary"),
        Submit("delete", "Удалить", css_class="btn-secondary"),
    ]

    class Meta:
        model = Message
        fields = "__all__"


class CreateMessageForm(MessageForm):
    layout_buttons = [Submit("submit", "Создать", css_class="btn-primary")]
    layout_header = "Создание нового сообщения"


class MailingForm(LayoutMixin, forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Редактирование рассылки"
    layout_buttons = [
        Submit("start", "Запустить рассылку", css_class="btn-primary"),
        Submit("submit", "Сохранить", css_class="btn-primary"),
        Submit("delete", "Удалить", css_class="btn-secondary"),
    ]

    class Meta:
        model = Mailing
        exclude = ("status",)


class CreateMailingForm(MailingForm):
    layout_buttons = [Submit("submit", "Создать", css_class="btn-primary")]
    layout_header = "Создание рассылки"


class CreateRaffleForm(LayoutMixin, forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Создание розыгрыша"
    layout_buttons = [Submit("submit", "Создать", css_class="btn-primary")]

    class Meta:
        model = Raffle
        exclude = ("winner",)


class PresentForm(LayoutMixin, forms.ModelForm):
    """
    Форма для редактирования пользователя в кабинете администратора
    """

    helper = FormHelper()
    helper.form_method = "post"
    helper.form_class = "theme-form"
    layout_header = "Основная информация о подарке"
    layout_buttons = [
        Submit("submit", "Сохранить", css_class="btn-primary"),
        Submit("delete", "Удалить", css_class="btn-secondary"),
    ]

    class Meta:
        model = Present
        fields = "__all__"


class CreatePresentForm(PresentForm):
    layout_buttons = [Submit("submit", "Создать", css_class="btn-primary")]
    layout_header = "Добавление нового подарка"
