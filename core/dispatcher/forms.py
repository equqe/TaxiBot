from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.gis import forms

from cabinet.forms import LayoutMixin
from .models import Settings, City, CostPerKm, CostPerBabyChair


class CityForm(LayoutMixin, forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"
    layout_header = "Настройки города"
    layout_buttons = [
        Submit("submit", "Сохранить", css_class="btn-primary"),
        Submit("delete", "Удалить", css_class="btn-secondary"),
    ]

    class Meta:
        model = City
        exclude = ("cost_per_km", "cost_per_baby_chair")


class CreateCityForm(LayoutMixin, forms.ModelForm):

    cost_per_km = forms.DecimalField(label="Стоимость за километр")
    cost_per_km__night_allowance = forms.DecimalField(
        label="Надбавочная стоимость ночью"
    )

    cost_per_baby_chair = forms.DecimalField(
        label="Надбавочная стоимость за детское кресло"
    )
    cost_per_baby_chair__night_allowance = forms.DecimalField(
        label="Ночная надбавка за детское кресло"
    )

    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Регистрация нового города"
    layout_buttons = [Submit("submit", "Зарегистрировать", css_class="btn-primary")]

    class Meta:
        model = City
        exclude = ("cost_per_km", "cost_per_baby_chair")


class CostPerKmForm(LayoutMixin, forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Стоимость за километр"
    layout_buttons = [
        Submit("submit__cost_per_km", "Сохранить", css_class="btn-primary")
    ]

    class Meta:
        model = CostPerKm
        fields = "__all__"


class CostPerBabyChairForm(LayoutMixin, forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Стоимость за детское кресло"
    layout_buttons = [
        Submit("submit__cost_per_baby_chair", "Сохранить", css_class="btn-primary")
    ]

    class Meta:
        model = CostPerBabyChair
        fields = "__all__"


class SettingsForm(LayoutMixin, forms.ModelForm):

    helper = FormHelper()
    helper.form_method = "post"

    layout_header = "Настройки диспетчера"
    layout_buttons = [
        Submit("submit__dispatcher", "Сохранить", css_class="btn-primary")
    ]

    class Meta:
        model = Settings
        fields = "__all__"
        widgets = {"web_app_map_center": forms.OSMWidget}
