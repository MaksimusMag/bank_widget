"""Модуль с сервисами."""

import re
from typing import Any, Dict, List


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для Инвесткопилки.

    Аргументы:
        month (str): Месяц в формате "YYYY-MM".
        transactions (List[Dict[str, Any]]): Список транзакций.
        limit (int): Шаг округления.

    Возвращает:
        float: Сумма для Инвесткопилки.
    """
    total = 0.0

    for transaction in transactions:
        date = transaction.get("Дата операции", "")
        if not date or not date.startswith(month):
            continue

        amount = transaction.get("Сумма операции", 0)
        if amount <= 0:
            continue

        rounded = ((amount + limit - 1) // limit) * limit
        total += rounded - amount

    return round(total, 2)


def simple_search(transactions: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Простой поиск по описанию или категории.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список транзакций.
        query (str): Строка для поиска.

    Возвращает:
        List[Dict[str, Any]]: Список найденных транзакций.
    """
    if not query:
        return transactions

    query_lower = query.lower()
    result = []

    for transaction in transactions:
        description = transaction.get("Описание", "").lower()
        category = transaction.get("Категория", "").lower()

        if query_lower in description or query_lower in category:
            result.append(transaction)

    return result


def search_by_phone(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Поиск транзакций по телефонным номерам в описании.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список транзакций.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций с телефонными номерами.
    """
    # Паттерн для поиска телефонных номеров в разных форматах
    pattern = re.compile(
        r"\+7\s?\d{3}\s?\d{2}\s?\d{2}\s?\d{2}|"  # +7 921 11-22-33
        r"\+7\s?\d{3}\s?\d{2}-\d{2}-\d{2}|"  # +7 921 11-22-33
        r"\+7\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}|"  # +7 (921) 111-22-33
        r"8\s?\(?\d{3}\)?\s?\d{3}\s?\d{2}\s?\d{2}|"  # 8 (921) 111-22-33
        r"8\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}|"  # 8 (921) 111-22-33
        r"7\s?\(?\d{3}\)?\s?\d{3}\s?\d{2}\s?\d{2}",  # 7 921 111-22-33
        re.IGNORECASE,
    )

    result = []

    for transaction in transactions:
        description = transaction.get("Описание", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def search_transfers_to_individuals(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Поиск переводов физическим лицам.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список транзакций.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций-переводов физлицам.
    """
    pattern = re.compile(r"[А-Я][а-я]+\s[А-Я]\.", re.UNICODE)

    result = []

    for transaction in transactions:
        category = transaction.get("Категория", "")
        description = transaction.get("Описание", "")

        if category == "Переводы" and pattern.search(description):
            result.append(transaction)

    return result


def profitable_categories(
    transactions: List[Dict[str, Any]], year: int, month: int
) -> Dict[str, float]:
    """
    Анализ выгодных категорий для кешбэка.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список транзакций.
        year (int): Год.
        month (int): Месяц.

    Возвращает:
        Dict[str, float]: Словарь с категориями и кешбэком.
    """
    month_str = f"{year:04d}-{month:02d}"
    filtered = []

    for transaction in transactions:
        date = transaction.get("Дата операции", "")
        if date and date.startswith(month_str):
            filtered.append(transaction)

    categories = {}
    for transaction in filtered:
        category = transaction.get("Категория", "Другое")
        cashback = transaction.get("Кешбэк", 0)

        if category not in categories:
            categories[category] = 0
        categories[category] += cashback

    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_categories[:3])
