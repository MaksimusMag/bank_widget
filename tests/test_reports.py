"""Тесты для модуля reports."""

import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


class TestSpendingByCategory:
    """Тесты для функции spending_by_category."""

    def test_spending_by_category_valid(self) -> None:
        """Тестирует траты по категории."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20", "2024-02-10"],
            "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"],
            "Сумма платежа": [100, 200, 50],
            "Описание": ["Покупка 1", "Покупка 2", "Такси"],
        }
        df = pd.DataFrame(data)
        result = spending_by_category(df, "Супермаркеты", "2024-02-01")
        assert len(result) == 2
        assert result["Сумма платежа"].sum() == 300

    def test_spending_by_category_empty(self) -> None:
        """Тестирует траты по категории с пустым датафреймом."""
        df = pd.DataFrame()
        result = spending_by_category(df, "Супермаркеты")
        assert result.empty


class TestSpendingByWeekday:
    """Тесты для функции spending_by_weekday."""

    def test_spending_by_weekday_valid(self) -> None:
        """Тестирует средние траты по дням недели."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-16", "2024-01-17"],
            "Сумма платежа": [100, 200, 50],
        }
        df = pd.DataFrame(data)
        result = spending_by_weekday(df, "2024-01-20")
        assert not result.empty
        assert "day" in result.columns
        assert "average_spent" in result.columns


class TestSpendingByWorkday:
    """Тесты для функции spending_by_workday."""

    def test_spending_by_workday_valid(self) -> None:
        """Тестирует траты в рабочие/выходные дни."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20", "2024-01-21"],
            "Сумма платежа": [100, 200, 50],
        }
        df = pd.DataFrame(data)
        result = spending_by_workday(df, "2024-01-22")
        assert not result.empty
        assert "day_type" in result.columns
        assert "average_spent" in result.columns
