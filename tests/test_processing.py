"""Тесты для модуля processing."""

import pytest

from src.constants import CANCELED_STATUS, EXECUTED_STATUS
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    @pytest.mark.parametrize(
        "target_state, expected_count, expected_ids",
        [
            (EXECUTED_STATUS, 2, [41428829, 939719570]),
            (CANCELED_STATUS, 2, [594226727, 615064591]),
            ("PENDING", 0, []),
        ],
    )
    def test_filter_by_state(
        self,
        sample_transactions,
        target_state: str,
        expected_count: int,
        expected_ids: list,
    ) -> None:
        """Тестирует фильтрацию по различным статусам."""
        result = filter_by_state(sample_transactions, target_state)
        assert len(result) == expected_count
        if expected_ids:
            result_ids = [item["id"] for item in result]
            assert result_ids == expected_ids

    def test_filter_by_state_default(self, sample_transactions) -> None:
        """Тестирует фильтрацию со статусом по умолчанию."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 2
        assert all(item["state"] == EXECUTED_STATUS for item in result)

    def test_filter_by_state_empty(self, empty_transactions) -> None:
        """Тестирует фильтрацию пустого списка."""
        result = filter_by_state(empty_transactions)
        assert result == []

    def test_filter_by_state_no_matching(self, sample_transactions) -> None:
        """Тестирует фильтрацию при отсутствии совпадений."""
        result = filter_by_state(sample_transactions, "PENDING")
        assert result == []


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_by_date_descending(self, sample_transactions) -> None:
        """Тестирует сортировку по убыванию."""
        result = sort_by_date(sample_transactions)
        assert len(result) == 4
        expected_order = [41428829, 615064591, 594226727, 939719570]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    def test_sort_by_date_ascending(self, sample_transactions) -> None:
        """Тестирует сортировку по возрастанию."""
        result = sort_by_date(sample_transactions, ascending_order=True)
        assert len(result) == 4
        expected_order = [939719570, 594226727, 615064591, 41428829]
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    def test_sort_by_date_empty(self, empty_transactions) -> None:
        """Тестирует сортировку пустого списка."""
        result = sort_by_date(empty_transactions)
        assert result == []
