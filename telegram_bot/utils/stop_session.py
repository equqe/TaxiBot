from loader import core


async def stop_session():
    """
        Останавливает сессию с CoreAPI после остановки чат-бота
    :param dp:
    :return:
    """

    await core.stop_session()
