import django_filters

from .managers import UserQuerySet
from .models import User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="iexact")
    is_driver = django_filters.BooleanFilter(
        field_name="is_driver", method="get_is_driver", label="Статус водителя"
    )
    is_active_driver = django_filters.BooleanFilter(
        field_name="is_active_driver",
        method="get_is_active_driver",
        label="Водитель на линии",
    )
    with_active_ride = django_filters.BooleanFilter(
        field_name="with_active_ride",
        method="get_with_active_ride",
        label="Водители с активными заказами",
    )
    phone_number = django_filters.CharFilter(method="filter_by_phone_number")

    @staticmethod
    def get_is_driver(queryset: UserQuerySet, name, value):
        if value is True:
            return queryset.drivers()
        elif value is False:
            return queryset.clients()

    @staticmethod
    def get_is_active_driver(queryset: UserQuerySet, name, value: bool):
        if value is True:
            return queryset.active_drivers()
        elif value is False:
            return queryset.inactive_drivers()

    @staticmethod
    def get_with_active_ride(queryset: UserQuerySet, name, value: bool):
        if value is True:
            return queryset.with_active_ride()
        elif value is False:
            return queryset.without_active_ride()

    @staticmethod
    def filter_by_phone_number(queryset: UserQuerySet, name, value: str):
        return queryset.filter(phone_number__icontains=value)

    class Meta:
        model = User
        fields = []
