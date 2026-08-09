"""Тесты для модуля processing_utils."""

from src.processing_utils import (
    filter_rub_transactions,
    filter_transactions_by_state,
    sort_transactions_by_date,
)


class TestFilterTransactionsByState:
    """Тесты для функции filter_transactions_by_state."""

    def test_filter_by_executed(self) -> None:
        """Тестирует фильтрацию по статусу EXECUTED."""
        transactions = [
            {"state": "EXECUTED"},
            {"state": "CANCELED"},
            {"state": "EXECUTED"},
        ]
        result = filter_transactions_by_state(transactions, "EXECUTED")
        assert len(result) == 2

    def test_filter_by_canceled(self) -> None:
        """Тестирует фильтрацию по статусу CANCELED."""
        transactions = [
            {"state": "EXECUTED"},
            {"state": "CANCELED"},
            {"state": "EXECUTED"},
        ]
        result = filter_transactions_by_state(transactions, "CANCELED")
        assert len(result) == 1

    def test_filter_case_insensitive(self) -> None:
        """Тестирует регистронезависимую фильтрацию."""
        transactions = [
            {"state": "EXECUTED"},
            {"state": "executed"},
            {"state": "CANCELED"},
        ]
        result = filter_transactions_by_state(transactions, "EXECUTED")
        assert len(result) == 2

    def test_filter_not_found(self) -> None:
        """Тестирует фильтрацию по несуществующему статусу."""
        transactions = [
            {"state": "EXECUTED"},
            {"state": "CANCELED"},
        ]
        result = filter_transactions_by_state(transactions, "PENDING")
        assert result == []

    def test_filter_empty(self) -> None:
        """Тестирует фильтрацию пустого списка."""
        result = filter_transactions_by_state([], "EXECUTED")
        assert result == []


class TestSortTransactionsByDate:
    """Тесты для функции sort_transactions_by_date."""

    def test_sort_ascending(self) -> None:
        """Тестирует сортировку по возрастанию."""
        transactions = [
            {"date": "2024-01-03"},
            {"date": "2024-01-01"},
            {"date": "2024-01-02"},
        ]
        result = sort_transactions_by_date(transactions, ascending=True)
        assert result[0]["date"] == "2024-01-01"
        assert result[1]["date"] == "2024-01-02"
        assert result[2]["date"] == "2024-01-03"

    def test_sort_descending(self) -> None:
        """Тестирует сортировку по убыванию."""
        transactions = [
            {"date": "2024-01-01"},
            {"date": "2024-01-03"},
            {"date": "2024-01-02"},
        ]
        result = sort_transactions_by_date(transactions, ascending=False)
        assert result[0]["date"] == "2024-01-03"
        assert result[1]["date"] == "2024-01-02"
        assert result[2]["date"] == "2024-01-01"

    def test_sort_empty(self) -> None:
        """Тестирует сортировку пустого списка."""
        result = sort_transactions_by_date([], ascending=True)
        assert result == []

    def test_sort_missing_date(self) -> None:
        """Тестирует сортировку при отсутствии даты."""
        transactions = [
            {"id": 1, "date": "2024-01-02"},
            {"id": 2},  # нет даты
            {"id": 3, "date": "2024-01-01"},
        ]
        result = sort_transactions_by_date(transactions, ascending=True)
        # Транзакции с датами должны быть отсортированы
        # Транзакция без даты должна быть в конце
        assert result[0]["id"] == 3  # 2024-01-01
        assert result[1]["id"] == 1  # 2024-01-02
        assert result[2]["id"] == 2  # без даты


class TestFilterRubTransactions:
    """Тесты для функции filter_rub_transactions."""

    def test_filter_rub(self) -> None:
        """Тестирует фильтрацию рублевых транзакций."""
        transactions = [
            {"operationAmount": {"currency": {"code": "RUB"}}},
            {"operationAmount": {"currency": {"code": "USD"}}},
            {"operationAmount": {"currency": {"code": "RUB"}}},
        ]
        result = filter_rub_transactions(transactions)
        assert len(result) == 2

    def test_filter_empty(self) -> None:
        """Тестирует фильтрацию пустого списка."""
        result = filter_rub_transactions([])
        assert result == []

    def test_filter_missing_currency(self) -> None:
        """Тестирует фильтрацию при отсутствии валюты."""
        transactions = [
            {"operationAmount": {}},
            {"operationAmount": {"currency": {"code": "RUB"}}},
        ]
        result = filter_rub_transactions(transactions)
        assert len(result) == 1
