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

    Пример:
        >>> transactions = [...]
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> for transaction in usd_transactions:
        ...     print(transaction["operationAmount"]["currency"]["code"])
        USD
        USD
        USD
    """
    for transaction in transactions:
        try:
            currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
            if currency == currency_code:
                yield transaction
        except (AttributeError, TypeError, KeyError):
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Генерирует описания транзакций по очереди.

    Аргументы:
        transactions (List[Dict]): Список словарей с транзакциями.

    Возвращает:
        Generator[str, None, None]: Генератор, выдающий описания транзакций.

    Пример:
        >>> transactions = [...]
        >>> descriptions = transaction_descriptions(transactions)
        >>> for desc in descriptions:
        ...     print(desc)
        Перевод организации
        Перевод со счета на счет
        Перевод со счета на счет
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

    Пример:
        >>> for card in card_number_generator(1, 5):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
        0000 0000 0000 0004
        0000 0000 0000 0005
    """
    MAX_CARD_NUMBER = 9999999999999999
    MIN_CARD_NUMBER = 1

    # Корректируем границы диапазона
    start = max(start, MIN_CARD_NUMBER)
    stop = min(stop, MAX_CARD_NUMBER)

    if start > stop:
        return

    for number in range(start, stop + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
