from ..serializers import UserSerializer, DriverSerializer, WorkDriverDaySerializer
from dispatcher.serializers import OrderSerializer
from rest_framework import serializers

# Данный пакет создан для того, чтобы избежать циркулярного импорта


class DriverExtendedSerializer(DriverSerializer):
    """
    Расширенный сериализатор для модели водителя
    """

    work_days = WorkDriverDaySerializer(many=True)


class UserExtendedSerializer(UserSerializer):
    """
    Расширенный сериалайзер пользователя
    """

    rides = OrderSerializer(many=True)
    driver = DriverExtendedSerializer()
    telegram_auth_token = serializers.SerializerMethodField()

    def get_telegram_auth_token(self, instance):
        return instance.telegram_auth_token.key


class UserExtendedSerializerWithPassword(UserExtendedSerializer):
    """
    Расширенный сериализатор для пользователя,
    который возвращает еще и пароль пользователя в личном кабинете
    """

    class Meta(UserExtendedSerializer.Meta):
        extra_kwargs = {}
