"""Утилиты для работы с данными."""

import json
from typing import Any, Dict

import pandas as pd


def read_transactions_from_excel(file_path: str) -> pd.DataFrame:
    """
    Читает данные о транзакциях из Excel-файла.

    Аргументы:
        file_path (str): Путь к Excel-файлу.

    Возвращает:
        pd.DataFrame: Датафрейм с транзакциями.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except (FileNotFoundError, ValueError, Exception):
        return pd.DataFrame()


def load_user_settings(file_path: str) -> Dict[str, Any]:
    """
    Загружает пользовательские настройки из JSON-файла.

    Аргументы:
        file_path (str): Путь к файлу настроек.

    Возвращает:
        Dict[str, Any]: Словарь с настройками.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data: Dict[str, Any] = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"user_currencies": ["USD", "EUR"], "user_stocks": []}


def filter_transactions_by_date(
    df: pd.DataFrame, date_str: str, period: str = "month"
) -> pd.DataFrame:
    """
    Фильтрует транзакции по дате.

    Аргументы:
        df (pd.DataFrame): Датафрейм с транзакциями.
        date_str (str): Дата в формате "YYYY-MM-DD".
        period (str): Период фильтрации.

    Возвращает:
        pd.DataFrame: Отфильтрованный датафрейм.
    """
    if df.empty:
        return df

    if "Дата операции" not in df.columns:
        return df

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    target_date = pd.to_datetime(date_str)

    if period == "month":
        start_date = target_date.replace(day=1)
    elif period == "week":
        start_date = target_date - pd.Timedelta(days=target_date.weekday())
    elif period == "year":
        start_date = target_date.replace(month=1, day=1)
    elif period == "all":
        start_date = pd.Timestamp.min  # минимальная дата
    else:
        start_date = target_date.replace(day=1)

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= target_date)
    return df.loc[mask]
