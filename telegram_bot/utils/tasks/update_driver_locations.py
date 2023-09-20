from loader import core, location_storage
from utils.misc.logging import update_locations_logger as logger


async def update_user_locations():
    """
    Фунция достает из оперативной памяти ID пользователей и их геопозиции
    """
    # logger.info('Началось обновление геопозиции пользователей...')
    user_ids = await location_storage.all_keys()
    # logger.info(f'Получены все ключи. Кол-во: {len(user_ids)}')
    if not user_ids:
        # logger.info('Обновление геопозиции прекращено, так как нет ключей')
        return
    result = []
    for key in user_ids:
        location = await location_storage.get_data(key)

        json_data = {"chat_id": int(key), "location": location.dict()}
        result.append(json_data)
    # logger.info('Сформирован объект json_data')
    await core.update_users_location(result)
    # logger.info('Геопозиция обновлена')
    await location_storage.reset_all()
    # logger.info('Хранилище геопозиций очищено!')
