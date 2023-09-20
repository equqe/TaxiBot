import aiohttp

from utils.misc.logging import logger


class BaseAPI:
    """
    Класс для API ядра системы. Должен наследовать абстрактные классы с методами
    """

    def __init__(self, token: str, base_url: str, headers: dict):
        """

        :param base_url: example: 'chatupper.com/api/'
        :param headers:
        """
        self.token = token
        self.BASE_URL = base_url
        self.headers = headers
        # self.start_session()

    async def start_session(self) -> None:
        """
        Запускает сессию, которая хранит в себе постоянные заголовки, такие как Authorization
        """
        self.headers["Authorization"] = f"EnvToken {self.token}"
        self.session = aiohttp.ClientSession(headers=self.headers)
        logger.info(f"ClientSession has started! <Token {self.token[:5]}>")

    async def stop_session(self) -> None:
        """
        Останавливает сессию
        """
        await self.session.close()
        logger.info(f"ClientSession has stoped! <Token {self.token[:5]}>")

    def base_url(self) -> str:
        """
                Возвращает стандартный URL
        :return:
        """
        return self.BASE_URL
