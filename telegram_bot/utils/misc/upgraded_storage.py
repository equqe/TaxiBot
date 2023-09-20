import pickle
import typing

from aiogram.contrib.fsm_storage.redis import RedisStorage2, STATE_DATA_KEY


class RedisPickleFSMStorage(RedisStorage2):
    """
    Save and load objects in memory with pickle
    """

    async def get_data(
        self,
        *,
        chat: typing.Union[str, int, None] = None,
        user: typing.Union[str, int, None] = None,
        default: typing.Optional[dict] = None
    ) -> typing.Dict:
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_DATA_KEY)
        redis = await self.redis()
        raw_result = await redis.get(key)
        if raw_result:
            return pickle.loads(raw_result)
        return default or {}

    async def set_data(
        self,
        *,
        chat: typing.Union[str, int, None] = None,
        user: typing.Union[str, int, None] = None,
        data: typing.Dict = None
    ):
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATE_DATA_KEY)
        redis = await self.redis()
        await redis.set(key, pickle.dumps(data), expire=self._data_ttl)
