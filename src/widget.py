"""Модуль для работы с виджетом банковских операций."""

from src.constants import ACCOUNT_TYPE_KEYWORDS
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Аргументы:
        account_card_info (str): Строка с типом и номером карты или счета.
                                 Примеры: "Visa Platinum 7000792289606361",
                                         "Счет 73654108430135874305"

    Возвращает:
        str: Строка с замаскированным номером.
    """
    if not account_card_info:
        return account_card_info

    info_parts = account_card_info.rsplit(" ", 1)

    if len(info_parts) != 2:
        return account_card_info

    card_type, card_number = info_parts[0], info_parts[1]

    if card_type.lower() in ACCOUNT_TYPE_KEYWORDS:
        return f"{card_type} {get_mask_account(card_number)}"
    else:
        return f"{card_type} {get_mask_card_number(card_number)}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Аргументы:
        date_string (str): Дата в формате "YYYY-MM-DDTHH:MM:SS.ffffff"

    Возвращает:
        str: Дата в формате "ДД.ММ.ГГГГ"
    """
    if not date_string or not date_string.strip():
        return date_string

    try:
        date_part = date_string.split("T")[0]

        if "-" not in date_part:
            return date_string

        parts = date_part.split("-")
        if len(parts) != 3:
            return date_string

        year, month, day = parts

        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return date_string

        return f"{day}.{month}.{year}"
    except (ValueError, AttributeError, IndexError):
        return date_string
