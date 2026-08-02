"""Модуль с генераторами для обработки данных транзакций."""

from typing import Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]:
    """
    Фильтрует транзакции по заданной валюте.

    Аргументы:
        transactions (List[Dict]): Список словарей с транзакциями.
        currency_code (str): Код валюты для фильтрации (например, "USD", "RUB").

    Возвращает:
        Iterator[Dict]: Итератор, выдающий транзакции с указанной валютой.
    """
    for transaction in transactions:
        try:
            currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
            if currency == currency_code:
                yield transaction
        except (AttributeError, TypeError, KeyError):
            continue


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Генерирует описания транзакций по очереди.

    Аргументы:
        transactions (List[Dict]): Список словарей с транзакциями.

    Возвращает:
        Generator[str, None, None]: Генератор, выдающий описания транзакций.
    """
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            if description:
                yield description
            else:
                yield "Описание отсутствует"
        except (AttributeError, TypeError):
            yield "Описание отсутствует"


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Аргументы:
        start (int): Начальное значение диапазона (включительно).
        stop (int): Конечное значение диапазона (включительно).

    Возвращает:
        Generator[str, None, None]: Генератор номеров карт в формате XXXX XXXX XXXX XXXX.
    """
    MAX_CARD_NUMBER = 9999999999999999
    MIN_CARD_NUMBER = 1

    start = max(start, MIN_CARD_NUMBER)
    stop = min(stop, MAX_CARD_NUMBER)

    if start > stop:
        return

    for number in range(start, stop + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
