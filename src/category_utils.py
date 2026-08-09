"""Модуль для подсчета категорий транзакций."""

from collections import Counter
from typing import Any, Dict, List


def count_transactions_by_category(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по категориям.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        categories (List[str]): Список категорий для подсчета.

    Возвращает:
        Dict[str, int]: Словарь с количеством транзакций по каждой категории.

    Пример:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод с карты на карту"},
        ...     {"description": "Перевод организации"},
        ... ]
        >>> categories = ["Перевод организации", "Перевод с карты на карту"]
        >>> count_transactions_by_category(transactions, categories)
        {"Перевод организации": 2, "Перевод с карты на карту": 1}
    """
    if not transactions or not categories:
        return {}

    # Создаем Counter с описаниями транзакций
    descriptions = [t.get("description", "") for t in transactions]
    counter = Counter(descriptions)

    # Фильтруем только нужные категории
    result = {category: counter.get(category, 0) for category in categories}

    return result
