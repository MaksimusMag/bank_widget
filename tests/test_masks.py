"""Тесты для модуля masks."""
"""Этот файл будет добавлен в репозиторий GitHub для проверки №1"""

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тестирует маскировку номера карты."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"


def test_get_mask_card_number_invalid() -> None:
    """Тестирует обработку некорректных номеров карт."""
    assert get_mask_card_number("") == ""
    assert get_mask_card_number("12345") == "12345"
    assert get_mask_card_number("123456789012345a") == "123456789012345a"


def test_get_mask_account() -> None:
    """Тестирует маскировку номера счета."""
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("1234567890") == "**7890"


def test_get_mask_account_invalid() -> None:
    """Тестирует обработку некорректных номеров счетов."""
    assert get_mask_account("") == ""
    assert get_mask_account("123") == "123"
