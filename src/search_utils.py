"""Модуль для поиска по транзакциям с использованием регулярных выражений."""

import re
from typing import Any, Dict, List


def search_transactions(
    transactions: List[Dict[str, Any]], search_query: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        search_query (str): Строка для поиска в описании.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций, в описании которых есть искомая строка.

    Пример:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод с карты на карту"},
        ... ]
        >>> search_transactions(transactions, "организации")
        [{"description": "Перевод организации"}]
    """
    if not search_query:
        return transactions

    pattern = re.compile(re.escape(search_query), re.IGNORECASE)
    result = [
        transaction
        for transaction in transactions
        if pattern.search(transaction.get("description", ""))
    ]
    return result
