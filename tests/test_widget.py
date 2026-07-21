"""Тесты для модуля widget."""

import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
            ("Visa Electron 1234567890123456", "Visa Electron 1234 56** **** 3456"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 64686473678894779589", "Счет **9589"),
            ("Счет 35383033474447895560", "Счет **5560"),
            ("счет 12345678901234567890", "счет **7890"),
        ]
    )
    def test_valid_card_and_account(self, input_data: str, expected: str) -> None:
        """Тестирует маскировку валидных карт и счетов."""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ("", ""),
            ("Visa", "Visa"),
            ("Счет", "Счет"),
            ("Card 123", "Card 123"),
            ("Visa Platinum 123", "Visa Platinum 123"),
            ("MasterCard abc", "MasterCard abc"),
            ("Счет abc", "Счет abc"),
            ("  ", "  "),
        ]
    )
    def test_invalid_input(self, input_data: str, expected: str) -> None:
        """Тестирует обработку некорректных входных данных."""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize(
        "input_data",
        [
            "Visa Platinum 1234567890123456",
            "MasterCard 1234567890123456",
            "Maestro 1234567890123456",
            "Счет 12345678901234567890",
            "Visa Gold 1234567890123456",
        ]
    )
    def test_various_card_types(self, input_data: str) -> None:
        """Тестирует различные типы карт и счетов."""
        result = mask_account_card(input_data)
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetDate:
    """Тесты для функции get_date."""

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2023-12-25T15:30:45.123456", "25.12.2023"),
            ("2024-01-01T00:00:00.000000", "01.01.2024"),
            ("2024-12-31T23:59:59.999999", "31.12.2024"),
            ("2024-06-15T12:00:00.000000", "15.06.2024"),
            ("2024-02-29T10:00:00.000000", "29.02.2024"),
            ("2024-07-19T09:30:00.123456", "19.07.2024"),
        ]
    )
    def test_valid_dates(self, input_date: str, expected: str) -> None:
        """Тестирует преобразование валидных дат."""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("", ""),
            ("invalid-date", "invalid-date"),
            ("2024/03/11T02:26:18", "2024/03/11T02:26:18"),
            ("2024-03-11", "11.03.2024"),  # Функция корректно преобразует
            ("T02:26:18.671407", "T02:26:18.671407"),
            ("2024-03-11T", "11.03.2024"),  # Исправлено: функция преобразует дату
            ("  ", "  "),
        ]
    )
    def test_invalid_dates(self, input_date: str, expected: str) -> None:
        """Тестирует обработку некорректных дат."""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize(
        "input_date, expected",
        [
            ("2024-01-01T00:00:00", "01.01.2024"),
            ("2024-12-31T23:59:59", "31.12.2024"),
            ("2024-06-15T12:00:00", "15.06.2024"),
        ]
    )
    def test_dates_without_microseconds(self, input_date: str, expected: str) -> None:
        """Тестирует даты без микросекунд."""
        assert get_date(input_date) == expected
