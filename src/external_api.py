"""Модуль для работы с внешними API."""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv(encoding="utf-8")


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Аргументы:
        transaction (Dict[str, Any]): Словарь с данными о транзакции.

    Возвращает:
        float: Сумма транзакции в рублях.
    """
    try:
        amount_str: str = transaction.get("operationAmount", {}).get("amount", "0")
        amount: float = float(amount_str)

        currency_code: str = (
            transaction.get("operationAmount", {}).get("currency", {}).get("code", "RUB")
        )

        if currency_code == "RUB":
            return amount

        if currency_code in ("USD", "EUR"):
            api_key: str = os.getenv("EXCHANGE_RATES_API_KEY", "")

            if not api_key:
                return amount

            url: str = "https://api.apilayer.com/exchangerates_data/convert"
            headers: Dict[str, str] = {"apikey": api_key}
            params: Dict[str, str] = {
                "from": currency_code,
                "to": "RUB",
                "amount": str(amount),
            }

            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()

                data: Dict[str, Any] = response.json()

                if data.get("success"):
                    return float(data.get("result", amount))

                return amount

            except (requests.RequestException, ValueError, KeyError):
                return amount

        return amount

    except (ValueError, AttributeError, TypeError):
        return 0.0
