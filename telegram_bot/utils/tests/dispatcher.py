def test_create_order(order_data=None):
    # Не сделан
    from api import CoreAPI
    from data import config

    if not order_data:
        pass
    core = CoreAPI(
        token=config.CORE_TOKEN,
        base_url=config.CORE_BASE_URL,
        headers=config.CORE_HEADERS,
    )
