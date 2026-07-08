"""Модуль для работы с виджетом банковских операций."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Аргументы:
        info (str): Строка с типом и номером карты или счета.

    Возвращает:
        str: Строка с замаскированным номером.

    """
    # Разделяем строку на тип и номер
    parts = info.rsplit(" ", 1)

    if len(parts) != 2:
        return info

    card_type, number = parts[0], parts[1]

    # Проверяем, является ли это счетом
    if card_type.lower() == "счет":
        return f"{card_type} {get_mask_account(number)}"
    else:
        # Для всех карт используем маскировку карт
        return f"{card_type} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Аргументы:
        date_string (str): Дата в формате "YYYY-MM-DDTHH:MM:SS.ffffff"

    Возвращает:
        str: Дата в формате "ДД.ММ.ГГГГ"
    """
    # Извлекаем часть с датой (до буквы T)
    date_part = date_string.split("T")[0]

    # Разделяем на год, месяц, день
    year, month, day = date_part.split("-")

    # Возвращаем в формате ДД.ММ.ГГГГ
    return f"{day}.{month}.{year}"
