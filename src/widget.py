"""Модуль для работы с виджетом банковских операций."""

from src.constants import ACCOUNT_TYPE_KEYWORDS
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа."""
    if not account_card_info:
        return account_card_info

    info_parts: list = account_card_info.rsplit(" ", 1)

    if len(info_parts) != 2:
        return account_card_info

    card_type: str = info_parts[0]
    card_number: str = info_parts[1]

    if card_type.lower() in ACCOUNT_TYPE_KEYWORDS:
        return f"{card_type} {get_mask_account(card_number)}"
    else:
        return f"{card_type} {get_mask_card_number(card_number)}"


def get_date(date_string: str) -> str:
    """Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ."""
    if not date_string or not date_string.strip():
        return date_string

    try:
        date_part: str = date_string.split("T")[0]

        if "-" not in date_part:
            return date_string

        parts: list = date_part.split("-")
        if len(parts) != 3:
            return date_string

        year: str = parts[0]
        month: str = parts[1]
        day: str = parts[2]

        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return date_string

        return f"{day}.{month}.{year}"
    except (ValueError, AttributeError, IndexError):
        return date_string
