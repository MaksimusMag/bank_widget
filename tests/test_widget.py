"""Тесты для модуля widget."""

from src.widget import get_date, mask_account_card


def test_mask_account_card_card() -> None:
    """Тестирует маскировку номеров карт."""
    visa_platinum_info = "Visa Platinum 7000792289606361"
    expected_visa_masked = "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card(visa_platinum_info) == expected_visa_masked

    maestro_info = "Maestro 1596837868705199"
    expected_maestro_masked = "Maestro 1596 83** **** 5199"
    assert mask_account_card(maestro_info) == expected_maestro_masked

    mastercard_info = "MasterCard 7158300734726758"
    expected_mastercard_masked = "MasterCard 7158 30** **** 6758"
    assert mask_account_card(mastercard_info) == expected_mastercard_masked

    visa_classic_info = "Visa Classic 6831982476737658"
    expected_visa_classic_masked = "Visa Classic 6831 98** **** 7658"
    assert mask_account_card(visa_classic_info) == expected_visa_classic_masked

    visa_gold_info = "Visa Gold 5999414228426353"
    expected_visa_gold_masked = "Visa Gold 5999 41** **** 6353"
    assert mask_account_card(visa_gold_info) == expected_visa_gold_masked


def test_mask_account_card_account() -> None:
    """Тестирует маскировку номеров счетов."""
    account_info_1 = "Счет 73654108430135874305"
    expected_account_masked_1 = "Счет **4305"
    assert mask_account_card(account_info_1) == expected_account_masked_1

    account_info_2 = "Счет 64686473678894779589"
    expected_account_masked_2 = "Счет **9589"
    assert mask_account_card(account_info_2) == expected_account_masked_2

    account_info_3 = "Счет 35383033474447895560"
    expected_account_masked_3 = "Счет **5560"
    assert mask_account_card(account_info_3) == expected_account_masked_3


def test_mask_account_card_invalid() -> None:
    """Тестирует обработку некорректных входных данных."""
    empty_info = ""
    assert mask_account_card(empty_info) == empty_info

    single_word_info = "Visa"
    assert mask_account_card(single_word_info) == single_word_info

    account_single_word = "Счет"
    assert mask_account_card(account_single_word) == account_single_word


def test_get_date() -> None:
    """Тестирует преобразование даты."""
    iso_date_1 = "2024-03-11T02:26:18.671407"
    expected_date_1 = "11.03.2024"
    assert get_date(iso_date_1) == expected_date_1

    iso_date_2 = "2023-12-25T15:30:45.123456"
    expected_date_2 = "25.12.2023"
    assert get_date(iso_date_2) == expected_date_2

    iso_date_3 = "2024-01-01T00:00:00.000000"
    expected_date_3 = "01.01.2024"
    assert get_date(iso_date_3) == expected_date_3
