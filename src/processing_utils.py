"""Модуль для обработки данных транзакций."""

from typing import Any, Dict, List


def filter_transactions_by_state(
    transactions: List[Dict[str, Any]], state: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        state (str): Статус для фильтрации.

    Возвращает:
        List[Dict[str, Any]]: Список отфильтрованных транзакций.
    """
    state_upper = state.upper()
    result = [
        transaction
        for transaction in transactions
        if transaction.get("state", "").upper() == state_upper
    ]
    return result


def sort_transactions_by_date(
    transactions: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        ascending (bool): Порядок сортировки. True - по возрастанию.

    Возвращает:
        List[Dict[str, Any]]: Отсортированный список транзакций.
    """
    # Разделяем транзакции на две группы: с датой и без даты
    with_date = [t for t in transactions if t.get("date")]
    without_date = [t for t in transactions if not t.get("date")]

    # Сортируем транзакции с датой
    sorted_with_date = sorted(
        with_date,
        key=lambda t: t.get("date", ""),
        reverse=not ascending,
    )

    # Возвращаем отсортированные с датой, затем без даты
    return sorted_with_date + without_date


def filter_rub_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции, оставляя только рублевые.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.

    Возвращает:
        List[Dict[str, Any]]: Список рублевых транзакций.
    """
    return [
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code", "") == "RUB"
    ]
