"""Модуль с утилитами для работы с данными."""

import json
from typing import Any, Dict, List


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные о транзакциях из JSON-файла.

    Аргументы:
        file_path (str): Путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, содержит не-список или не найден,
                              возвращается пустой список.

    Пример:
        >>> transactions = read_transactions_from_json("data/operations.json")
        >>> len(transactions)
        6
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)

            if not isinstance(data, list):
                return []

            return data

    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []
