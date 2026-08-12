"""Тесты для модуля utils."""

import json
import tempfile
from unittest.mock import patch

import pandas as pd

from src.utils import (
    filter_transactions_by_date,
    load_user_settings,
    read_transactions_from_excel,
)


class TestReadTransactionsFromExcel:
    """Тесты для функции read_transactions_from_excel."""

    @patch("src.utils.pd.read_excel")
    def test_read_excel_valid(self, mock_read_excel) -> None:
        """Тестирует чтение валидного Excel-файла."""
        mock_df = pd.DataFrame({"id": [1, 2]})
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("test.xlsx")
        assert not result.empty
        assert len(result) == 2

    @patch("src.utils.pd.read_excel")
    def test_read_excel_not_found(self, mock_read_excel) -> None:
        """Тестирует чтение несуществующего файла."""
        mock_read_excel.side_effect = FileNotFoundError
        result = read_transactions_from_excel("non_existent.xlsx")
        assert result.empty


class TestLoadUserSettings:
    """Тесты для функции load_user_settings."""

    def test_load_user_settings_valid(self) -> None:
        """Тестирует загрузку валидного файла настроек."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump({"user_currencies": ["USD"], "user_stocks": ["AAPL"]}, tmp)
            tmp_path = tmp.name

        result = load_user_settings(tmp_path)
        assert result["user_currencies"] == ["USD"]
        assert result["user_stocks"] == ["AAPL"]

    def test_load_user_settings_not_found(self) -> None:
        """Тестирует загрузку несуществующего файла."""
        result = load_user_settings("non_existent.json")
        assert result["user_currencies"] == ["USD", "EUR"]
        assert result["user_stocks"] == []


class TestFilterTransactionsByDate:
    """Тесты для функции filter_transactions_by_date."""

    def test_filter_by_month(self) -> None:
        """Тестирует фильтрацию по месяцу."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20", "2024-02-10"],
        }
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        result = filter_transactions_by_date(df, "2024-01-20", "month")
        assert len(result) == 2

    def test_filter_by_week(self) -> None:
        """Тестирует фильтрацию по неделе."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20", "2024-01-25"],
        }
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        result = filter_transactions_by_date(df, "2024-01-20", "week")
        assert len(result) == 2

    def test_filter_by_year(self) -> None:
        """Тестирует фильтрацию по году."""
        data = {
            "Дата операции": ["2023-12-15", "2024-01-15", "2024-02-20"],
        }
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        result = filter_transactions_by_date(df, "2024-06-20", "year")
        assert len(result) == 2

    def test_filter_all(self) -> None:
        """Тестирует фильтрацию 'all'."""
        data = {
            "Дата операции": ["2023-12-15", "2024-01-15", "2024-02-20"],
        }
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])

        result = filter_transactions_by_date(df, "2024-01-20", "all")
        assert len(result) == 2

    def test_filter_empty_df(self) -> None:
        """Тестирует фильтрацию пустого датафрейма."""
        df = pd.DataFrame()
        result = filter_transactions_by_date(df, "2024-01-20")
        assert result.empty
