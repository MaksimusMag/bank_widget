"""Модуль для обработки данных банковских операций."""

from typing import Dict, List, Union

from src.constants import EXECUTED_STATUS

Transaction = Dict[str, Union[str, int]]
TransactionList = List[Transaction]


def filter_by_state(
    transaction_data: TransactionList, target_state: str = EXECUTED_STATUS
) -> TransactionList:
    """Фильтрует список транзакций по значению ключа 'state'."""
    if not transaction_data:
        return []

    filtered_transactions: TransactionList = [
        transaction for transaction in transaction_data if transaction.get("state") == target_state
    ]

    return filtered_transactions


def sort_by_date(
    transaction_data: TransactionList, ascending_order: bool = False
) -> TransactionList:
    """Сортирует список транзакций по дате."""
    if not transaction_data:
        return []

    sorted_transactions: TransactionList = sorted(
        transaction_data,
        key=lambda transaction: transaction.get("date", ""),
        reverse=not ascending_order,
    )

    return sorted_transactions
