"""Модуль с декораторами для логирования."""

import functools
import logging
import os
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функций."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name: str = func.__name__

            logger = logging.getLogger(func_name)
            logger.setLevel(logging.INFO)

            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            if filename:
                try:
                    log_dir: str = os.path.dirname(filename)
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
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            try:
                result: Any = func(*args, **kwargs)
                logger.info(f"{func_name} ok")
                return result
            except Exception as e:
                error_msg: str = f"{func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                logger.error(error_msg)
                raise

        return wrapper

    return decorator
