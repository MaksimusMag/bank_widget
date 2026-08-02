"""Модуль для обработки данных банковских операций."""

from typing import Dict, List, Union

from src.constants import EXECUTED_STATUS

Transaction = Dict[str, Union[str, int]]
TransactionList = List[Transaction]


def filter_by_state(
    transaction_data: TransactionList, target_state: str = EXECUTED_STATUS
) -> TransactionList:
    """
    Фильтрует список транзакций по значению ключа 'state'.

    Аргументы:
        transaction_data (TransactionList): Список словарей с транзакциями.
        target_state (str): Значение для фильтрации по ключу 'state'.
                            По умолчанию 'EXECUTED'.

    Возвращает:
        TransactionList: Новый список словарей, содержащий только те
                         транзакции, у которых ключ 'state' соответствует
                         указанному значению.
    """
    if not transaction_data:
        return []

    filtered_transactions = [
        transaction for transaction in transaction_data if transaction.get("state") == target_state
    ]

    return filtered_transactions


def sort_by_date(
    transaction_data: TransactionList, ascending_order: bool = False
) -> TransactionList:
    """
    Сортирует список транзакций по дате.

    Аргументы:
        transaction_data (TransactionList): Список словарей с транзакциями.
        ascending_order (bool): Порядок сортировки. False - убывание (сначала новые),
                                True - возрастание (сначала старые).
                                По умолчанию False.

    Возвращает:
        TransactionList: Новый список словарей, отсортированный по дате.
    """
    if not transaction_data:
        return []

    sorted_transactions = sorted(
        transaction_data,
        key=lambda transaction: transaction.get("date", ""),
        reverse=not ascending_order,
    )

    return sorted_transactions
