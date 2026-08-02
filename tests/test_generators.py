"""Тесты для модуля generators."""

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    @pytest.mark.parametrize(
        "currency_code, expected_count",
        [
            ("USD", 3),
            ("RUB", 2),
            ("EUR", 0),
        ],
    )
    def test_filter_by_currency(
        self, sample_transactions_with_currency, currency_code: str, expected_count: int
    ) -> None:
        """Тестирует фильтрацию по различным валютам."""
        result = list(filter_by_currency(sample_transactions_with_currency, currency_code))
        assert len(result) == expected_count

    def test_filter_by_currency_empty(self, empty_transactions_list) -> None:
        """Тестирует фильтрацию пустого списка."""
        result = list(filter_by_currency(empty_transactions_list, "USD"))
        assert result == []


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_transaction_descriptions(self, sample_transactions_with_currency) -> None:
        """Тестирует получение описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions_with_currency))
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        assert descriptions == expected

    def test_transaction_descriptions_empty(self, empty_transactions_list) -> None:
        """Тестирует получение описаний из пустого списка."""
        descriptions = list(transaction_descriptions(empty_transactions_list))
        assert descriptions == []


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize(
        "start, stop, expected",
        [
            (
                1,
                5,
                [
                    "0000 0000 0000 0001",
                    "0000 0000 0000 0002",
                    "0000 0000 0000 0003",
                    "0000 0000 0000 0004",
                    "0000 0000 0000 0005",
                ],
            ),
            (1, 1, ["0000 0000 0000 0001"]),
        ],
    )
    def test_card_number_generator_valid_range(self, start: int, stop: int, expected: list) -> None:
        """Тестирует генерацию номеров карт в заданном диапазоне."""
        result = list(card_number_generator(start, stop))
        assert result == expected

    def test_card_number_generator_format(self) -> None:
        """Тестирует корректность форматирования номеров карт."""
        result = list(card_number_generator(1, 3))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]
        assert result == expected
        for card in result:
            groups = card.split()
            assert len(groups) == 4
            for group in groups:
                assert len(group) == 4
                assert group.isdigit()
