"""Модуль с декораторами для логирования."""

import functools
import logging
import os
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Аргументы:
        filename (Optional[str]): Имя файла для записи логов.
                                  Если не указан, логи выводятся в консоль.

    Возвращает:
        Callable: Декорированная функция.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            # Настройка логирования
            logger = logging.getLogger(func_name)
            logger.setLevel(logging.INFO)

            # Удаляем существующие обработчики
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            # Создаем форматтер
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            if filename:
                # Логирование в файл
                try:
                    log_dir = os.path.dirname(filename)
                    if log_dir and not os.path.exists(log_dir):
                        os.makedirs(log_dir)
                    file_handler = logging.FileHandler(filename, encoding="utf-8")
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                except (OSError, PermissionError) as e:
                    console_handler = logging.StreamHandler()
                    console_handler.setFormatter(formatter)
                    logger.addHandler(console_handler)
                    logger.error(f"Не удалось создать файл {filename}: {e}")
            else:
                # Логирование в консоль (stderr)
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func_name} ok")
                return result
            except Exception as e:
                error_msg = f"{func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                logger.error(error_msg)
                raise

        return wrapper

    return decorator
