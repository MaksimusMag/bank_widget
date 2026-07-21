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

    Примеры:
        >>> sample_transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED',
        ...      'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED',
        ...      'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED',
        ...      'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> filter_by_state(sample_transactions)
        [{'id': 41428829, 'state': 'EXECUTED',
          'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED',
          'date': '2018-06-30T02:08:58.425572'}]

        >>> filter_by_state(sample_transactions, 'CANCELED')
        [{'id': 594226727, 'state': 'CANCELED',
          'date': '2018-09-12T21:27:25.241689'}]
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

    Примеры:
        >>> sample_transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED',
        ...      'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED',
        ...      'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED',
        ...      'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> sort_by_date(sample_transactions)
        [{'id': 41428829, ...}, {'id': 594226727, ...},
         {'id': 939719570, ...}]

        >>> sort_by_date(sample_transactions, ascending_order=True)
        [{'id': 939719570, ...}, {'id': 594226727, ...},
         {'id': 41428829, ...}]
    """
    if not transaction_data:
        return []

    sorted_transactions = sorted(
        transaction_data,
        key=lambda transaction: transaction.get("date", ""),
        reverse=not ascending_order,
    )

    return sorted_transactions
