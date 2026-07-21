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

    Примеры:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'

        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    if not account_card_info:
        return account_card_info

    info_parts = account_card_info.rsplit(' ', 1)

    if len(info_parts) != 2:
        return account_card_info

    card_type, card_number = info_parts[0], info_parts[1]

    if card_type.lower() in ACCOUNT_TYPE_KEYWORDS:
        return f"{card_type} {get_mask_account(card_number)}"
    else:
        return f"{card_type} {get_mask_card_number(card_number)}"


def get_date(iso_date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Аргументы:
        iso_date_string (str): Дата в формате "YYYY-MM-DDTHH:MM:SS.ffffff"

    Возвращает:
        str: Дата в формате "ДД.ММ.ГГГГ"

    Примеры:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    if not iso_date_string:
        return iso_date_string

    try:
        # Извлекаем часть с датой (до буквы T)
        date_part = iso_date_string.split('T')[0]

        # Разделяем на год, месяц, день
        year, month, day = date_part.split('-')

        # Проверяем, что все части состоят из цифр
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return iso_date_string

        # Возвращаем в формате ДД.ММ.ГГГГ
        return f"{day}.{month}.{year}"
    except (ValueError, AttributeError, IndexError):
        # Если произошла ошибка при разборе, возвращаем исходную строку
        return iso_date_string
