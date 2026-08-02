"""Модуль с генераторами для обработки данных транзакций."""

from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency_code: str
) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте."""
    for transaction in transactions:
        try:
            currency: str = (
                transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
            )
            if currency == currency_code:
                yield transaction
        except (AttributeError, TypeError, KeyError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Генерирует описания транзакций по очереди."""
    for transaction in transactions:
        try:
            description: str = transaction.get("description", "")
            if description:
                yield description
            else:
                yield "Описание отсутствует"
        except (AttributeError, TypeError):
            yield "Описание отсутствует"


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в заданном диапазоне."""
    MAX_CARD_NUMBER: int = 9999999999999999
    MIN_CARD_NUMBER: int = 1

    start = max(start, MIN_CARD_NUMBER)
    stop = min(stop, MAX_CARD_NUMBER)

    if start > stop:
        return

    for number in range(start, stop + 1):
        formatted: str = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
