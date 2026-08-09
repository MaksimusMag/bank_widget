"""Тесты для модуля reading."""

import csv
import os
import tempfile
from unittest.mock import Mock, patch

from src.reading import read_transactions_from_csv, read_transactions_from_excel


class TestReadTransactionsFromCSV:
    """Тесты для функции read_transactions_from_csv."""

    def test_read_valid_csv(self) -> None:
        """Тестирует чтение валидного CSV-файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["id", "amount", "currency"])
            writer.writerow(["1", "100", "USD"])
            writer.writerow(["2", "200", "RUB"])
            tmp_path = tmp.name

        try:
            result = read_transactions_from_csv(tmp_path)
            assert len(result) == 2
            assert result[0]["id"] == "1"
            assert result[0]["amount"] == "100"
            assert result[0]["currency"] == "USD"
        finally:
            os.remove(tmp_path)

    def test_read_empty_csv(self) -> None:
        """Тестирует чтение пустого CSV-файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("")
            tmp_path = tmp.name

        try:
            result = read_transactions_from_csv(tmp_path)
            assert result == []
        finally:
            os.remove(tmp_path)

    def test_read_csv_file_not_found(self) -> None:
        """Тестирует чтение несуществующего файла."""
        result = read_transactions_from_csv("non_existent_file.csv")
        assert result == []

    def test_read_csv_only_headers(self) -> None:
        """Тестирует чтение CSV-файла только с заголовками."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["id", "amount", "currency"])
            tmp_path = tmp.name

        try:
            result = read_transactions_from_csv(tmp_path)
            assert result == []
        finally:
            os.remove(tmp_path)


class TestReadTransactionsFromExcel:
    """Тесты для функции read_transactions_from_excel."""

    @patch("src.reading.pd.read_excel")
    def test_read_valid_excel(self, mock_read_excel: Mock) -> None:
        """Тестирует чтение валидного Excel-файла."""
        mock_df = Mock()
        mock_df.empty = False
        mock_df.to_dict.return_value = [
            {"id": 1, "amount": 100, "currency": "USD"},
            {"id": 2, "amount": 200, "currency": "RUB"},
        ]
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("test.xlsx")
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["amount"] == 100
        assert result[0]["currency"] == "USD"

    @patch("src.reading.pd.read_excel")
    def test_read_empty_excel(self, mock_read_excel: Mock) -> None:
        """Тестирует чтение пустого Excel-файла."""
        mock_df = Mock()
        mock_df.empty = True
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("empty.xlsx")
        assert result == []

    @patch("src.reading.pd.read_excel")
    def test_read_excel_file_not_found(self, mock_read_excel: Mock) -> None:
        """Тестирует чтение несуществующего файла."""
        mock_read_excel.side_effect = FileNotFoundError

        result = read_transactions_from_excel("non_existent.xlsx")
        assert result == []

    @patch("src.reading.pd.read_excel")
    def test_read_excel_error(self, mock_read_excel: Mock) -> None:
        """Тестирует обработку ошибки при чтении Excel."""
        mock_read_excel.side_effect = Exception("Test error")

        result = read_transactions_from_excel("error.xlsx")
        assert result == []
