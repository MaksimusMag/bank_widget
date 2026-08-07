"""Модуль с утилитами для работы с данными."""

import json
import logging
import os
from typing import Any, Dict, List

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем директорию для логов, если её нет
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка обработчика для записи в файл
file_handler = logging.FileHandler(f"{log_dir}/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настройка форматера
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные о транзакциях из JSON-файла.

    Аргументы:
        file_path (str): Путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, содержит не-список или не найден,
                              возвращается пустой список.
    """
    logger.info(f"Попытка чтения файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: Any = json.load(file)

            if not isinstance(data, list):
                logger.error(f"Файл {file_path} содержит не список")
                return []

            logger.info(f"Успешно прочитано {len(data)} транзакций из {file_path}")
            return data

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []

    except ValueError as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []
