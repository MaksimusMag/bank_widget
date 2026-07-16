"""Модуль для обработки данных банковских операций."""

from typing import Dict, List


def filter_by_state(
    transactions: List[Dict[str, str]], state: str = "EXECUTED"
) -> List[Dict[str, str]]:
    """
    Фильтрует список транзакций по значению ключа 'state'.

    Аргументы:
        transactions (List[Dict[str, str]]): Список словарей с транзакциями.
        state (str): Значение для фильтрации по ключу 'state'.
                     По умолчанию 'EXECUTED'.

    Возвращает:
        List[Dict[str, str]]: Новый список словарей, содержащий только те
                              транзакции, у которых ключ 'state' соответствует
                              указанному значению.

    Примеры:
        >>> transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED',
        ...      'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED',
        ...      'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED',
        ...      'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> filter_by_state(transactions)
        [{'id': 41428829, 'state': 'EXECUTED',
          'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED',
          'date': '2018-06-30T02:08:58.425572'}]

        >>> filter_by_state(transactions, 'CANCELED')
        [{'id': 594226727, 'state': 'CANCELED',
          'date': '2018-09-12T21:27:25.241689'}]
    """
    if not transactions:
        return []

    return [item for item in transactions if item.get("state") == state]


def sort_by_date(
    transactions: List[Dict[str, str]], ascending: bool = False
) -> List[Dict[str, str]]:
    """
    Сортирует список транзакций по дате.

    Аргументы:
        transactions (List[Dict[str, str]]): Список словарей с транзакциями.
        ascending (bool): Порядок сортировки. False - убывание (сначала новые),
                          True - возрастание (сначала старые).
                          По умолчанию False.

    Возвращает:
        List[Dict[str, str]]: Новый список словарей, отсортированный по дате.

    Примеры:
        >>> transactions = [
        ...     {'id': 41428829, 'state': 'EXECUTED',
        ...      'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED',
        ...      'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED',
        ...      'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> sort_by_date(transactions)  # по умолчанию убывание
        [{'id': 41428829, ...}, {'id': 594226727, ...},
         {'id': 939719570, ...}]

        >>> sort_by_date(transactions, ascending=True)  # возрастание
        [{'id': 939719570, ...}, {'id': 594226727, ...},
         {'id': 41428829, ...}]
    """
    if not transactions:
        return []

    return sorted(
        transactions,
        key=lambda x: x.get("date", ""),
        reverse=not ascending,
    )
