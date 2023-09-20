from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import ModelActionsPermission
from cabinet.exceptions import USER_NOT_REGISTERED
from cabinet.models import User
from cabinet.serializers import TelegramDataSerializer
from dispatcher.models import City, Order
from .exceptions import COUPON_DOES_NOT_EXIST
from .models import Coupon
from .serializers import (
    CouponSerializer,
    PickCouponFromTelegramSerializer,
    PresentSerializer,
)
from .utils.coupon import give_coupon_to_user


class UserCouponsAPI(generics.GenericAPIView):
    """
    НЕ ЗАКОНЧЕННО
    """

    serializer_class = TelegramDataSerializer
    permission_classes = [ModelActionsPermission]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat_id = serializer.data.chat_id
        coupons = User.objects.get(telegram_data__chat_id=chat_id).coupons

        return Response(CouponSerializer(coupons, many=True))


@csrf_exempt
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def pick_coupon_from_telegram(request):
    """
    Принимает chat_id телеграмм пользователя и уникальный код купона
    Применяет купон к указанному пользователю или возвращает ошибку
    """
    data = JSONParser().parse(request)

    serializer = PickCouponFromTelegramSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    chat_id = serializer.validated_data.get("chat_id")
    coupon_code = serializer.validated_data.get("coupon_code")
    try:
        user = User.objects.get(telegram_data__chat_id=chat_id)
    except User.DoesNotExist:
        return JsonResponse({"detail": USER_NOT_REGISTERED.code})
    try:
        coupon = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return JsonResponse({"detail": COUPON_DOES_NOT_EXIST})
    try:
        give_coupon_to_user(user, coupon)
    except Exception as E:
        print(E.args)
        return JsonResponse({"detail": E.args[0]})

    return JsonResponse(CouponSerializer(coupon).data)


@csrf_exempt
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def get_present_from_order(request):
    data = JSONParser().parse(request)
    order_id = data.get("order_id")
    present = None
    try:

        order = Order.objects.select_related(
            "finish_address", "finish_address__city", "address", "address__city"
        ).get(pk=order_id)
        if order.finish_address:
            present = order.finish_address.city.presents.order_by("?").first()
        if not present:
            present = order.address.city.presents.order_by("?").first()

    except City.DoesNotExist:
        return JsonResponse({"detail": "bad_request"})
    except Order.DoesNotExist:
        return JsonResponse({"detail": "bad_request"})

    response_data = PresentSerializer(present).data if present else {}
    return JsonResponse(response_data)
