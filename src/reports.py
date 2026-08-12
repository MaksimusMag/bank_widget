"""Модуль для генерации отчетов."""

import functools
import json
import os
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar

import pandas as pd

F = TypeVar("F", bound=Callable[..., Any])


def report_decorator(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор для сохранения отчетов в файл.

    Аргументы:
        filename (Optional[str]): Имя файла для сохранения.

    Возвращает:
        Callable: Декорированная функция.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            if filename:
                output_file = filename
            else:
                output_file = (
                    f"report_{func.__name__}_" f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )

            os.makedirs("reports", exist_ok=True)
            file_path = os.path.join("reports", output_file)

            with open(file_path, "w", encoding="utf-8") as f:
                if isinstance(result, pd.DataFrame):
                    result.to_json(f, orient="records", force_ascii=False, indent=2)
                elif isinstance(result, (dict, list)):
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(result))

            return result

        return wrapper  # type: ignore

    return decorator


@report_decorator()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца.

    Аргументы:
        transactions (pd.DataFrame): Датафрейм с транзакциями.
        category (str): Название категории.
        date (Optional[str]): Дата в формате "YYYY-MM-DD".

    Возвращает:
        pd.DataFrame: Траты по категории за последние 3 месяца.
    """
    if transactions.empty or "Дата операции" not in transactions.columns:
        return pd.DataFrame()

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    target_date = pd.to_datetime(date)
    start_date = target_date - pd.Timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= target_date)
    filtered = df.loc[mask]

    if "Категория" in filtered.columns and "Сумма платежа" in filtered.columns:
        result = filtered[filtered["Категория"] == category]
        return result[["Дата операции", "Сумма платежа", "Описание"]]

    return pd.DataFrame()


@report_decorator()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты по дням недели за последние 3 месяца.

    Аргументы:
        transactions (pd.DataFrame): Датафрейм с транзакциями.
        date (Optional[str]): Дата в формате "YYYY-MM-DD".

    Возвращает:
        pd.DataFrame: Средние траты по дням недели.
    """
    if transactions.empty or "Дата операции" not in transactions.columns:
        return pd.DataFrame()

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    target_date = pd.to_datetime(date)
    start_date = target_date - pd.Timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= target_date)
    filtered = df.loc[mask]

    if "Сумма платежа" in filtered.columns:
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        result = []

        for day in days:
            avg = filtered[filtered["Дата операции"].dt.day_name(locale="ru_RU") == day][
                "Сумма платежа"
            ].mean()
            result.append({"day": day, "average_spent": round(avg, 2) if not pd.isna(avg) else 0})

        return pd.DataFrame(result)

    return pd.DataFrame()


@report_decorator()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочие и выходные дни за последние 3 месяца.

    Аргументы:
        transactions (pd.DataFrame): Датафрейм с транзакциями.
        date (Optional[str]): Дата в формате "YYYY-MM-DD".

    Возвращает:
        pd.DataFrame: Средние траты в рабочие и выходные дни.
    """
    if transactions.empty or "Дата операции" not in transactions.columns:
        return pd.DataFrame()

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    target_date = pd.to_datetime(date)
    start_date = target_date - pd.Timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= target_date)
    filtered = df.loc[mask]

    if "Сумма платежа" in filtered.columns:
        workdays = [0, 1, 2, 3, 4]
        weekend = [5, 6]

        workday_avg = filtered[filtered["Дата операции"].dt.weekday.isin(workdays)][
            "Сумма платежа"
        ].mean()

        weekend_avg = filtered[filtered["Дата операции"].dt.weekday.isin(weekend)][
            "Сумма платежа"
        ].mean()

        return pd.DataFrame(
            [
                {
                    "day_type": "Рабочий день",
                    "average_spent": round(workday_avg, 2) if not pd.isna(workday_avg) else 0,
                },
                {
                    "day_type": "Выходной день",
                    "average_spent": round(weekend_avg, 2) if not pd.isna(weekend_avg) else 0,
                },
            ]
        )

    return pd.DataFrame()
