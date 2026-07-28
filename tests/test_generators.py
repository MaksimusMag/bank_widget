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
        "currency_code, expected_count, expected_ids",
        [
            ("USD", 3, [939719570, 142264268, 895315941]),
            ("RUB", 2, [873106923, 594226727]),
            ("EUR", 0, []),
        ],
    )
    def test_filter_by_currency(
        self,
        sample_transactions_with_currency,
        currency_code: str,
        expected_count: int,
        expected_ids: list,
    ) -> None:
        """Тестирует фильтрацию по различным валютам."""
        result = list(filter_by_currency(sample_transactions_with_currency, currency_code))
        assert len(result) == expected_count
        if expected_ids:
            result_ids = [item["id"] for item in result]
            assert result_ids == expected_ids

    def test_filter_by_currency_empty(self, empty_transactions_list) -> None:
        """Тестирует фильтрацию пустого списка."""
        result = list(filter_by_currency(empty_transactions_list, "USD"))
        assert result == []

    def test_filter_by_currency_no_matching(self, sample_transactions_with_currency) -> None:
        """Тестирует фильтрацию при отсутствии совпадений."""
        result = list(filter_by_currency(sample_transactions_with_currency, "EUR"))
        assert result == []

    def test_filter_by_currency_without_currency(self, transactions_without_currency) -> None:
        """Тестирует фильтрацию транзакций без валюты."""
        result = list(filter_by_currency(transactions_without_currency, "USD"))
        assert result == []

    def test_filter_by_currency_iterator(self, sample_transactions_with_currency) -> None:
        """Тестирует, что функция возвращает итератор."""
        result = filter_by_currency(sample_transactions_with_currency, "USD")
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_filter_by_currency_generator_works(self, sample_transactions_with_currency) -> None:
        """Тестирует работу генератора с next()."""
        result = filter_by_currency(sample_transactions_with_currency, "USD")
        first = next(result)
        assert first["id"] == 939719570
        second = next(result)
        assert second["id"] == 142264268
        third = next(result)
        assert third["id"] == 895315941


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

    def test_transaction_descriptions_missing_description(self) -> None:
        """Тестирует получение описаний при отсутствии поля description."""
        transactions = [
            {"id": 1},
            {"id": 2, "description": "Описание есть"},
            {"id": 3},
        ]
        descriptions = list(transaction_descriptions(transactions))
        expected = ["Описание отсутствует", "Описание есть", "Описание отсутствует"]
        assert descriptions == expected

    def test_transaction_descriptions_generator(self, sample_transactions_with_currency) -> None:
        """Тестирует, что функция возвращает генератор."""
        result = transaction_descriptions(sample_transactions_with_currency)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_transaction_descriptions_generator_works(
        self, sample_transactions_with_currency
    ) -> None:
        """Тестирует работу генератора с next()."""
        result = transaction_descriptions(sample_transactions_with_currency)
        first = next(result)
        assert first == "Перевод организации"
        second = next(result)
        assert second == "Перевод со счета на счет"


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
            (
                9999999999999990,
                9999999999999995,
                [
                    "9999 9999 9999 9990",
                    "9999 9999 9999 9991",
                    "9999 9999 9999 9992",
                    "9999 9999 9999 9993",
                    "9999 9999 9999 9994",
                    "9999 9999 9999 9995",
                ],
            ),
            (1, 1, ["0000 0000 0000 0001"]),
            (10, 12, ["0000 0000 0000 0010", "0000 0000 0000 0011", "0000 0000 0000 0012"]),
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

    def test_card_number_generator_start_less_than_one(self) -> None:
        """Тестирует обработку start меньше 1."""
        result = list(card_number_generator(0, 3))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]
        assert result == expected

    def test_card_number_generator_stop_greater_than_max(self) -> None:
        """Тестирует обработку stop больше максимального значения."""
        max_card = 9999999999999999
        result = list(card_number_generator(max_card - 2, max_card + 5))
        expected = [
            "9999 9999 9999 9997",
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]
        assert result == expected

    def test_card_number_generator_start_greater_than_stop(self) -> None:
        """Тестирует случай, когда start > stop."""
        result = list(card_number_generator(10, 5))
        assert result == []

    def test_card_number_generator_generator(self) -> None:
        """Тестирует, что функция возвращает генератор."""
        result = card_number_generator(1, 5)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_card_number_generator_works(self) -> None:
        """Тестирует работу генератора с next()."""
        result = card_number_generator(1, 3)
        first = next(result)
        assert first == "0000 0000 0000 0001"
        second = next(result)
        assert second == "0000 0000 0000 0002"
        third = next(result)
        assert third == "0000 0000 0000 0003"

    @pytest.mark.parametrize(
        "start, stop, expected_count",
        [
            (1, 5, 5),
            (100, 110, 11),
            (9999999999999990, 9999999999999995, 6),
        ],
    )
    def test_card_number_generator_count(self, start: int, stop: int, expected_count: int) -> None:
        """Тестирует количество сгенерированных номеров."""
        result = list(card_number_generator(start, stop))
        assert len(result) == expected_count


class TestFilterByCurrencyExceptions:
    """Тесты для обработки исключений в filter_by_currency."""

    def test_filter_by_currency_with_missing_currency_field(self) -> None:
        """Тестирует обработку транзакций без поля currency."""
        transactions = [
            {"id": 1, "operationAmount": {}},  # Нет поля currency
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_by_currency_with_invalid_structure(self) -> None:
        """Тестирует обработку транзакций с некорректной структурой."""
        transactions = [
            {"id": 1},  # Нет operationAmount
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestTransactionDescriptionsExceptions:
    """Тесты для обработки исключений в transaction_descriptions."""

    def test_transaction_descriptions_with_missing_description(self) -> None:
        """Тестирует обработку транзакций без поля description."""
        transactions = [
            {"id": 1},  # Нет description
            {"id": 2, "description": "Описание есть"},
        ]
        result = list(transaction_descriptions(transactions))
        expected = ["Описание отсутствует", "Описание есть"]
        assert result == expected

    def test_transaction_descriptions_with_empty_description(self) -> None:
        """Тестирует обработку транзакций с пустым description."""
        transactions = [
            {"id": 1, "description": ""},
            {"id": 2, "description": "Описание есть"},
        ]
        result = list(transaction_descriptions(transactions))
        expected = ["Описание отсутствует", "Описание есть"]
        assert result == expected
