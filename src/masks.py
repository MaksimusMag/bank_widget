"""Модуль для маскировки номеров карт и счетов."""

from src.constants import (
    ACCOUNT_NUMBER_MIN_LENGTH,
    CARD_DISPLAY_FIRST_FOUR,
    CARD_DISPLAY_NEXT_TWO,
    CARD_NUMBER_LENGTH,
)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Аргументы:
        card_number (str): Номер карты в виде строки (16 цифр).

    Возвращает:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX.

    Пример:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    if not card_number:
        return card_number

    if len(card_number) != CARD_NUMBER_LENGTH:
        return card_number

    if not card_number.isdigit():
        return card_number

    first_four_digits = card_number[:CARD_DISPLAY_FIRST_FOUR]
    next_two_digits = card_number[CARD_DISPLAY_FIRST_FOUR:CARD_DISPLAY_NEXT_TWO]
    last_four_digits = card_number[-CARD_DISPLAY_FIRST_FOUR:]

    return f"{first_four_digits} {next_two_digits}** **** {last_four_digits}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Аргументы:
        account_number (str): Номер счета в виде строки.

    Возвращает:
        str: Замаскированный номер счета в формате **XXXX (последние 4 цифры).

    Пример:
        >>> get_mask_account("73654108430135874305")
        '**4305'
    """
    if not account_number:
        return account_number

    # Проверяем, что строка состоит только из цифр
    if not account_number.isdigit():
        return account_number

    if len(account_number) < ACCOUNT_NUMBER_MIN_LENGTH:
        return account_number

    last_four_digits = account_number[-ACCOUNT_NUMBER_MIN_LENGTH:]
    return f"**{last_four_digits}"
