import logging

from pyqiwi import Wallet

LAST_QIWI_UPDATED_ID = None  # Используется для избежания лишних запросов в ядро
LAST_DATETIME_REQUEST = None


async def qiwi_transactions_handler(qiwi: Wallet):
    global LAST_QIWI_UPDATED_ID, LAST_DATETIME_REQUEST

    logging.info("Начинается процедура запроса новых платежей")
    # Делаем запрос на последние транзакции, начиная с определенной даты
    transactions = qiwi.history(rows=50, start_date=LAST_DATETIME_REQUEST).get(
        "transactions"
    )
    # Берём только новые транзакции
    new_transactions = await get_new_transactions(LAST_QIWI_UPDATED_ID, transactions)
    if not new_transactions:
        logging.info("Нет новых платежей")
        return
    for t in new_transactions:
        print(f"<Transaction {t.txn_id} | {t.comment}>")

    if new_transactions:
        LAST_QIWI_UPDATED_ID = transactions[0].txn_id


async def get_new_transactions(last_id, transactions: list) -> list:
    for i in range(len(transactions)):
        if transactions[i].txn_id == last_id:
            return transactions[:i]
