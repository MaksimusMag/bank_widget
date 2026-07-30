"""Тесты для модуля masks."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1234567890123456", "1234 56** **** 3456"),
            ("0000000000000000", "0000 00** **** 0000"),
            ("1111222233334444", "1111 22** **** 4444"),
            ("9999888877776666", "9999 88** **** 6666"),
        ],
    )
    def test_valid_card_numbers(self, card_number: str, expected: str) -> None:
        """Тестирует маскировку валидных номеров карт."""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "card_number",
        [
            "",  # пустая строка
            "12345",  # слишком короткий
            "12345678901234567",  # слишком длинный
            "123456789012345",  # 15 цифр
            "1234567890123456a",  # содержит букву
            "abcdefghijklmnop",  # только буквы
            "1234 5678 9012 3456",  # с пробелами
            "1234-5678-9012-3456",  # с дефисами
        ],
    )
    def test_invalid_card_numbers(self, card_number: str) -> None:
        """Тестирует обработку некорректных номеров карт."""
        assert get_mask_card_number(card_number) == card_number


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654108430135874305", "**4305"),
            ("1234567890", "**7890"),
            ("11111111111111111111", "**1111"),
            ("000000000000", "**0000"),
            ("9876543210", "**3210"),
            ("12345678901234567890", "**7890"),
        ],
    )
    def test_valid_account_numbers(self, account_number: str, expected: str) -> None:
        """Тестирует маскировку валидных номеров счетов."""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize(
        "account_number",
        [
            "",  # пустая строка
            "123",  # меньше 4 символов
            "12",  # 2 символа
            "1",  # 1 символ
            "abc",  # буквы
        ],
    )
    def test_invalid_account_numbers(self, account_number: str) -> None:
        """Тестирует обработку некорректных номеров счетов."""
        assert get_mask_account(account_number) == account_number

    @pytest.mark.parametrize(
        "account_number",
        [
            "123a",  # содержит букву
            "12 34",  # с пробелом
        ],
    )
    def test_invalid_account_numbers_with_digits(self, account_number: str) -> None:
        """Тестирует обработку номеров счетов с нецифровыми символами."""
        assert get_mask_account(account_number) == account_number

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("1234", "**1234"),
            ("12345", "**2345"),
            ("123456", "**3456"),
        ],
    )
    def test_edge_cases(self, account_number: str, expected: str) -> None:
        """Тестирует граничные случаи (минимальная длина)."""
        assert get_mask_account(account_number) == expected
