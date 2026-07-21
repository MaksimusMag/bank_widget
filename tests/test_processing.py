"""Тесты для модуля processing."""

import pytest

from src.constants import CANCELED_STATUS, EXECUTED_STATUS, PENDING_STATUS
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    @pytest.mark.parametrize(
        "target_state, expected_count, expected_ids",
        [
            (EXECUTED_STATUS, 2, [41428829, 939719570]),
            (CANCELED_STATUS, 2, [594226727, 615064591]),
            (PENDING_STATUS, 0, []),
            ("INVALID_STATUS", 0, []),
        ]
    )
    def test_filter_by_state(
        self,
        sample_transactions,
        target_state: str,
        expected_count: int,
        expected_ids: list
    ) -> None:
        """Тестирует фильтрацию по различным статусам."""
        result = filter_by_state(sample_transactions, target_state)
        assert len(result) == expected_count
        if expected_ids:
            result_ids = [item["id"] for item in result]
            assert result_ids == expected_ids

    def test_filter_by_state_default(
        self,
        sample_transactions
    ) -> None:
        """Тестирует фильтрацию со статусом по умолчанию (EXECUTED)."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 2
        assert all(item["state"] == EXECUTED_STATUS for item in result)
        assert result[0]["id"] == 41428829
        assert result[1]["id"] == 939719570

    def test_filter_by_state_empty(self, empty_transactions) -> None:
        """Тестирует фильтрацию пустого списка."""
        result = filter_by_state(empty_transactions)
        assert result == []

    def test_filter_by_state_no_matching(
        self,
        sample_transactions
    ) -> None:
        """Тестирует фильтрацию при отсутствии совпадений."""
        result = filter_by_state(sample_transactions, "PENDING")
        assert result == []

    def test_filter_by_state_with_missing_state(
        self,
        sample_transactions
    ) -> None:
        """Тестирует фильтрацию при отсутствии ключа state."""
        transactions_without_state = [
            {"id": 1, "date": "2024-01-01"},
            {"id": 2, "state": EXECUTED_STATUS, "date": "2024-01-02"},
        ]
        result = filter_by_state(transactions_without_state)
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_by_date_descending(
        self,
        sample_transactions
    ) -> None:
        """Тестирует сортировку по убыванию (по умолчанию)."""
        result = sort_by_date(sample_transactions)
        assert len(result) == 4
        expected_order = [41428829, 615064591, 594226727, 939719570]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    def test_sort_by_date_ascending(
        self,
        sample_transactions
    ) -> None:
        """Тестирует сортировку по возрастанию."""
        result = sort_by_date(sample_transactions, ascending_order=True)
        assert len(result) == 4
        expected_order = [939719570, 594226727, 615064591, 41428829]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    def test_sort_by_date_same_dates(
        self,
        transactions_with_same_dates
    ) -> None:
        """Тестирует сортировку при одинаковых датах."""
        result = sort_by_date(transactions_with_same_dates)
        assert len(result) == 3
        # При одинаковых датах порядок сохраняется как в исходном списке
        expected_ids = [1, 2, 3]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids

    def test_sort_by_date_empty(self, empty_transactions) -> None:
        """Тестирует сортировку пустого списка."""
        result = sort_by_date(empty_transactions)
        assert result == []

    def test_sort_by_date_missing_dates(
        self,
        transactions_with_missing_dates
    ) -> None:
        """Тестирует сортировку при отсутствии дат у некоторых записей."""
        result = sort_by_date(transactions_with_missing_dates)
        assert len(result) == 3
        # Записи с датами должны быть отсортированы, пустая дата в конце
        expected_ids = [1, 3, 2]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids

    def test_sort_by_date_ascending_missing_dates(
        self,
        transactions_with_missing_dates
    ) -> None:
        """Тестирует сортировку по возрастанию при отсутствии дат."""
        result = sort_by_date(
            transactions_with_missing_dates,
            ascending_order=True
        )
        assert len(result) == 3
        # При возрастании: пустая строка идет первой при сортировке строк
        expected_ids = [2, 3, 1]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids

    def test_sort_by_date_invalid_dates(
        self,
        invalid_date_transactions
    ) -> None:
        """Тестирует сортировку с нестандартными форматами дат."""
        result = sort_by_date(invalid_date_transactions)
        assert len(result) == 3
        # Сортировка по строковому значению (лексикографическая)
        expected_ids = [3, 2, 1]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids

    @pytest.mark.parametrize(
        "ascending, expected_ids",
        [
            (False, [1, 2, 3]),  # убывание
            (True, [3, 2, 1]),   # возрастание
        ]
    )
    def test_sort_by_date_various_orders(
        self,
        sample_transactions_simple,
        ascending: bool,
        expected_ids: list
    ) -> None:
        """Тестирует сортировку в разных порядках."""
        result = sort_by_date(
            sample_transactions_simple,
            ascending_order=ascending
        )
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_ids


@pytest.fixture
def sample_transactions_simple() -> list:
    """
    Простая фикстура с транзакциями для тестов сортировки.
    """
    return [
        {"id": 1, "date": "2024-01-03T00:00:00.000000"},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
