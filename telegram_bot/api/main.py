from models.cabinet import Settings as CabinetSettings
from models.dispatcher import Settings as DispatcherSettings
from .base import BaseAPI
from .orders import OrderAPIMethods
from .referral import ReferralAPIMethods
from .users import UserAPIMethods
from .utils import get_request


class CoreAPI(BaseAPI, UserAPIMethods, OrderAPIMethods, ReferralAPIMethods):
    """
    Класс объединяющий все классы для API
    """

    async def get_all_settings(self):
        response = await get_request(
            session=self.session,
            url=self.base_url() + "getAllSettings/",
            headers=self.headers,
        )

        json_data = await response.json()
        return {
            "cabinet_settings": CabinetSettings.parse_obj(
                json_data["cabinet_settings"]
            ),
            "dispatcher_settings": DispatcherSettings.parse_obj(
                json_data["dispatcher_settings"]
            ),
        }
