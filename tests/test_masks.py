"""Тесты для модуля masks."""

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тестирует маскировку номера карты."""
    valid_card_number = "7000792289606361"
    expected_masked_card = "7000 79** **** 6361"
    assert get_mask_card_number(valid_card_number) == expected_masked_card

    another_card_number = "1234567890123456"
    expected_another_masked = "1234 56** **** 3456"
    assert get_mask_card_number(another_card_number) == expected_another_masked


def test_get_mask_card_number_invalid() -> None:
    """Тестирует обработку некорректных номеров карт."""
    empty_card_number = ""
    assert get_mask_card_number(empty_card_number) == empty_card_number

    short_card_number = "12345"
    assert get_mask_card_number(short_card_number) == short_card_number

    invalid_card_number = "123456789012345a"
    assert get_mask_card_number(invalid_card_number) == invalid_card_number


def test_get_mask_account() -> None:
    """Тестирует маскировку номера счета."""
    valid_account_number = "73654108430135874305"
    expected_masked_account = "**4305"
    assert get_mask_account(valid_account_number) == expected_masked_account

    another_account_number = "1234567890"
    expected_another_masked = "**7890"
    assert get_mask_account(another_account_number) == expected_another_masked


def test_get_mask_account_invalid() -> None:
    """Тестирует обработку некорректных номеров счетов."""
    empty_account_number = ""
    assert get_mask_account(empty_account_number) == empty_account_number

    short_account_number = "123"
    assert get_mask_account(short_account_number) == short_account_number
