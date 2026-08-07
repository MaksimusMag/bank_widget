"""Модуль для маскировки номеров карт и счетов."""

import logging
import os

from src.constants import (
    ACCOUNT_NUMBER_MIN_LENGTH,
    CARD_DISPLAY_FIRST_FOUR,
    CARD_DISPLAY_NEXT_TWO,
    CARD_NUMBER_LENGTH,
)

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем директорию для логов, если её нет
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка обработчика для записи в файл
file_handler = logging.FileHandler(f"{log_dir}/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настройка форматера
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Аргументы:
        card_number (str): Номер карты в виде строки (16 цифр).

    Возвращает:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX.
    """
    logger.debug(f"Вызов get_mask_card_number с аргументом: {card_number}")

    if not card_number:
        logger.warning("get_mask_card_number: пустая строка")
        return card_number

    if len(card_number) != CARD_NUMBER_LENGTH:
        logger.warning(f"get_mask_card_number: некорректная длина {len(card_number)}")
        return card_number

    if not card_number.isdigit():
        logger.warning(f"get_mask_card_number: содержит нецифровые символы: {card_number}")
        return card_number

    first_four_digits: str = card_number[:CARD_DISPLAY_FIRST_FOUR]
    next_two_digits: str = card_number[CARD_DISPLAY_FIRST_FOUR:CARD_DISPLAY_NEXT_TWO]
    last_four_digits: str = card_number[-CARD_DISPLAY_FIRST_FOUR:]

    result: str = f"{first_four_digits} {next_two_digits}** **** {last_four_digits}"
    logger.info(f"get_mask_card_number: успешно замаскирован номер {card_number} -> {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Аргументы:
        account_number (str): Номер счета в виде строки.

    Возвращает:
        str: Замаскированный номер счета в формате **XXXX (последние 4 цифры).
    """
    logger.debug(f"Вызов get_mask_account с аргументом: {account_number}")

    if not account_number:
        logger.warning("get_mask_account: пустая строка")
        return account_number

    if not account_number.isdigit():
        logger.warning(f"get_mask_account: содержит нецифровые символы: {account_number}")
        return account_number

    if len(account_number) < ACCOUNT_NUMBER_MIN_LENGTH:
        logger.warning(f"get_mask_account: длина {len(account_number)} меньше минимальной")
        return account_number

    last_four_digits: str = account_number[-ACCOUNT_NUMBER_MIN_LENGTH:]
    result: str = f"**{last_four_digits}"
    logger.info(f"get_mask_account: успешно замаскирован счет {account_number} -> {result}")
    return result
