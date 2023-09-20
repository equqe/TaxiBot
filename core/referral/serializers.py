from cabinet.models import User
from django.conf import settings as config
from rest_framework import serializers

from . import models


class CouponSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для купонов
    """

    class Meta:
        model = models.Coupon
        exclude = ("quantity",)


class MessageSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    def get_photo_url(self, instance):
        if instance.photo:
            return config.BASE_URL + instance.photo.url

    def get_video_url(self, instance):
        if instance.video:
            return config.BASE_URL + instance.video.url

    class Meta:
        model = models.Message
        fields = "__all__"


class MailingSerializer(serializers.Serializer):
    """
    Сериализатор данных для бота, автоматически конвертирует группу в список telegram айдишников
    """

    message = MessageSerializer()
    telegram_ids = serializers.SerializerMethodField()

    def get_telegram_ids(self, instance):
        users = User.objects.by_usergroup(instance.user_group)
        return list(users.telegram_ids())

    class Meta:
        fields = ("message", "telegram_ids")


class PickCouponFromTelegramSerializer(serializers.Serializer):

    chat_id = serializers.IntegerField()
    coupon_code = serializers.CharField()


class PresentSerializer(serializers.ModelSerializer):

    message = MessageSerializer()
    city = serializers.SerializerMethodField()

    def get_city(self, instance):
        from dispatcher.serializers import CitySerializer

        return CitySerializer(instance.city).data

    class Meta:
        model = models.Present
        fields = "__all__"
