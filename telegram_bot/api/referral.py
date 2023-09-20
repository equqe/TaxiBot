from api.utils import post_request
from models.dispatcher import Coupon
from models.referral import initialize_present


class ReferralAPIMethods:
    async def pick_coupon(self, chat_id, coupon_code):
        """
        Отправляет запрос в ядро и применяет купон к пользователю
        Работает только для зарегистрированных пользователей
        """
        json_data = {"chat_id": chat_id, "coupon_code": coupon_code}
        response = await post_request(
            session=self.session,
            url=self.base_url() + "coupons/pickCouponFromTelegram/",
            json_data=json_data,
            headers=self.headers,
        )

        return Coupon.parse_obj(await response.json())

    async def get_present_by_order_id(self, order_id: int):
        json_data = {"order_id": order_id}
        response = await post_request(
            session=self.session,
            url=self.base_url() + "presents/getPresentFromOrder/",
            json_data=json_data,
            headers=self.headers,
        )

        return await initialize_present(await response.json())
