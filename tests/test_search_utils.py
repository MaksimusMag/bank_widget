"""Тесты для модуля search_utils."""

from src.search_utils import search_transactions


class TestSearchTransactions:
    """Тесты для функции search_transactions."""

    def test_search_found(self) -> None:
        """Тестирует поиск по существующей строке."""
        transactions = [
            {"description": "Перевод организации"},
            {"description": "Перевод с карты на карту"},
            {"description": "Оплата услуг"},
        ]
        result = search_transactions(transactions, "Перевод")
        assert len(result) == 2
        assert result[0]["description"] == "Перевод организации"
        assert result[1]["description"] == "Перевод с карты на карту"

    def test_search_not_found(self) -> None:
        """Тестирует поиск по отсутствующей строке."""
        transactions = [
            {"description": "Перевод организации"},
            {"description": "Перевод с карты на карту"},
        ]
        result = search_transactions(transactions, "Оплата")
        assert result == []

    def test_search_case_insensitive(self) -> None:
        """Тестирует регистронезависимый поиск."""
        transactions = [
            {"description": "Перевод организации"},
            {"description": "перевод с карты на карту"},
        ]
        result = search_transactions(transactions, "перевод")
        assert len(result) == 2

    def test_search_empty_query(self) -> None:
        """Тестирует поиск с пустой строкой."""
        transactions = [
            {"description": "Перевод организации"},
            {"description": "Перевод с карты на карту"},
        ]
        result = search_transactions(transactions, "")
        assert result == transactions

    def test_search_empty_transactions(self) -> None:
        """Тестирует поиск в пустом списке."""
        result = search_transactions([], "Перевод")
        assert result == []

    def test_search_missing_description(self) -> None:
        """Тестирует поиск при отсутствии поля description."""
        transactions = [
            {"id": 1},
            {"description": "Перевод организации"},
        ]
        result = search_transactions(transactions, "Перевод")
        assert len(result) == 1
        assert result[0]["description"] == "Перевод организации"
