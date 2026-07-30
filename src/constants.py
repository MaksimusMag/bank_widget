"""Константы для банковского виджета."""

from typing import Final

# Длины номеров
CARD_NUMBER_LENGTH: Final[int] = 16
ACCOUNT_NUMBER_MIN_LENGTH: Final[int] = 4

# Индексы для маскировки карт
CARD_DISPLAY_FIRST_FOUR: Final[int] = 4
CARD_DISPLAY_NEXT_TWO: Final[int] = 6

# Статусы транзакций
EXECUTED_STATUS: Final[str] = "EXECUTED"
CANCELED_STATUS: Final[str] = "CANCELED"
PENDING_STATUS: Final[str] = "PENDING"

# Типы счетов для определения
ACCOUNT_TYPE_KEYWORDS: Final[tuple] = ("счет", "счёт", "account", "acc")
