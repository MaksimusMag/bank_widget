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
    # Для примера используем фиксированные курсы
    # В реальном проекте здесь должен быть API-запрос
    rates = {"USD": 85.50, "EUR": 92.30}
    return [{"currency": c, "rate": rates.get(c, 0.0)} for c in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Возвращает цены акций."""
    # Для примера используем фиксированные цены
    # В реальном проекте здесь должен быть API-запрос
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


def aggregate_expenses(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Агрегирует расходы для страницы событий.

    Аргументы:
        df (pd.DataFrame): Датафрейм с транзакциями.

    Возвращает:
        Dict[str, Any]: Словарь с агрегированными расходами.
    """
    if df.empty or "Сумма платежа" not in df.columns:
        return {"total_amount": 0, "main": [], "transfers_and_cash": []}

    # Фильтруем только расходы (отрицательные суммы)
    expenses_df = df[df["Сумма платежа"] < 0].copy()
    if expenses_df.empty:
        return {"total_amount": 0, "main": [], "transfers_and_cash": []}

    # Суммируем расходы по категориям
    category_totals = (
        expenses_df.groupby("Категория")["Сумма платежа"].sum().abs().round().to_dict()
    )

    total_amount = sum(category_totals.values())

    # Разделяем на основные категории и "Переводы и наличные"
    transfers_and_cash = {}
    main_categories = {}

    for category, amount in category_totals.items():
        if category in ["Переводы", "Наличные"]:
            transfers_and_cash[category] = amount
        else:
            main_categories[category] = amount

    # Сортируем основные категории по убыванию
    sorted_main = sorted(main_categories.items(), key=lambda x: x[1], reverse=True)

    # Топ-7 категорий
    top_7 = sorted_main[:7]
    other_amount = sum(amount for _, amount in sorted_main[7:])

    # Формируем результат
    main_result = [{"category": cat, "amount": int(amount)} for cat, amount in top_7]

    if other_amount > 0:
        main_result.append({"category": "Остальное", "amount": int(other_amount)})

    transfers_result = [
        {"category": cat, "amount": int(amount)}
        for cat, amount in sorted(transfers_and_cash.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "total_amount": int(total_amount),
        "main": main_result,
        "transfers_and_cash": transfers_result,
    }


def aggregate_income(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Агрегирует поступления для страницы событий.

    Аргументы:
        df (pd.DataFrame): Датафрейм с транзакциями.

    Возвращает:
        Dict[str, Any]: Словарь с агрегированными поступлениями.
    """
    if df.empty or "Сумма платежа" not in df.columns:
        return {"total_amount": 0, "main": []}

    # Фильтруем только поступления (положительные суммы)
    income_df = df[df["Сумма платежа"] > 0].copy()
    if income_df.empty:
        return {"total_amount": 0, "main": []}

    # Суммируем поступления по категориям
    category_totals = income_df.groupby("Категория")["Сумма платежа"].sum().round().to_dict()

    total_amount = sum(category_totals.values())

    # Сортируем по убыванию
    sorted_income = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    main_result = [{"category": cat, "amount": int(amount)} for cat, amount in sorted_income]

    return {
        "total_amount": int(total_amount),
        "main": main_result,
    }


def events_page(date_str: str, period: str = "month") -> Dict[str, Any]:
    """
    Страница событий.

    Аргументы:
        date_str (str): Дата в формате "YYYY-MM-DD".
        period (str): Период фильтрации ("month", "week", "year", "all").

    Возвращает:
        Dict[str, Any]: JSON-ответ для страницы событий.
    """
    df = pd.read_excel("data/operations.xls")
    if df.empty:
        return {"error": "No data available"}

    # Фильтруем данные по дате и периоду
    filtered_df = filter_transactions_by_date(df, date_str, period)

    # Загружаем настройки пользователя
    settings = load_user_settings("user_settings.json")
    currencies = settings.get("user_currencies", ["USD", "EUR"])
    stocks = settings.get("user_stocks", [])

    return {
        "expenses": aggregate_expenses(filtered_df),
        "income": aggregate_income(filtered_df),
        "currency_rates": get_currency_rates(currencies),
        "stock_prices": get_stock_prices(stocks),
    }
