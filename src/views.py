"""Модуль для генерации JSON-ответов для веб-страниц."""

from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from src.utils import filter_transactions_by_date, load_user_settings


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_info(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Возвращает информацию по картам."""
    if df.empty or "Номер карты" not in df.columns:
        return []

    cards = df[df["Номер карты"].notna()]
    result = []

    for _, group in cards.groupby("Номер карты"):
        total_spent = group["Сумма платежа"].sum()
        cashback = group["Кешбэк"].sum() if "Кешбэк" in group.columns else 0

        result.append(
            {
                "last_digits": str(group["Номер карты"].iloc[0])[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2),
            }
        )

    return result


def get_top_transactions(df: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
    """Возвращает топ-N транзакций по сумме."""
    if df.empty or "Сумма платежа" not in df.columns:
        return []

    sorted_df = df.sort_values("Сумма платежа", ascending=False).head(n)
    result = []

    for _, row in sorted_df.iterrows():
        date = row.get("Дата операции", "")
        if isinstance(date, pd.Timestamp):
            date = date.strftime("%d.%m.%Y")

        result.append(
            {
                "date": date,
                "amount": round(row["Сумма платежа"], 2),
                "category": row.get("Категория", ""),
                "description": row.get("Описание", ""),
            }
        )

    return result


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Возвращает курсы валют."""
    rates = {"USD": 85.50, "EUR": 92.30}
    return [{"currency": c, "rate": rates.get(c, 0.0)} for c in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Возвращает цены акций."""
    prices = {"AAPL": 175.50, "AMZN": 180.00, "GOOGL": 140.00, "MSFT": 330.00, "TSLA": 240.00}
    return [{"stock": s, "price": prices.get(s, 0.0)} for s in stocks]


def main_page(date_str: str) -> Dict[str, Any]:
    """
    Главная страница.

    Аргументы:
        date_str (str): Дата в формате "YYYY-MM-DD".

    Возвращает:
        Dict[str, Any]: JSON-ответ для главной страницы.
    """
    df = pd.read_excel("data/operations.xls")
    if df.empty:
        return {"error": "No data available"}

    filtered_df = filter_transactions_by_date(df, date_str, "month")

    settings = load_user_settings("user_settings.json")
    currencies = settings.get("user_currencies", ["USD", "EUR"])
    stocks = settings.get("user_stocks", [])

    return {
        "greeting": get_greeting(),
        "cards": get_card_info(filtered_df),
        "top_transactions": get_top_transactions(filtered_df, 5),
        "currency_rates": get_currency_rates(currencies),
        "stock_prices": get_stock_prices(stocks),
    }


def events_page(date_str: str, period: str = "month") -> Dict[str, Any]:
    """
    Страница событий.

    Аргументы:
        date_str (str): Дата в формате "YYYY-MM-DD".
        period (str): Период фильтрации.

    Возвращает:
        Dict[str, Any]: JSON-ответ для страницы событий.
    """
    df = pd.read_excel("data/operations.xls")
    if df.empty:
        return {"error": "No data available"}

    # Фильтруем данные по дате и периоду (результат будет использован позже)
    _ = filter_transactions_by_date(df, date_str, period)

    return {
        "expenses": {
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": [],
        },
        "income": {
            "total_amount": 0,
            "main": [],
        },
        "currency_rates": get_currency_rates(["USD", "EUR"]),
        "stock_prices": get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]),
    }
