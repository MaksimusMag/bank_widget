"""Тесты для модуля category_utils."""

from src.category_utils import count_transactions_by_category


class TestCountTransactionsByCategory:
    """Тесты для функции count_transactions_by_category."""

    def test_count_valid(self) -> None:
        """Тестирует подсчет по категориям."""
        transactions = [
            {"description": "Перевод организации"},
            {"description": "Перевод с карты на карту"},
            {"description": "Перевод организации"},
            {"description": "Оплата услуг"},
        ]
        categories = ["Перевод организации", "Перевод с карты на карту"]
        result = count_transactions_by_category(transactions, categories)
        assert result == {"Перевод организации": 2, "Перевод с карты на карту": 1}

    def test_count_empty_transactions(self) -> None:
        """Тестирует подсчет с пустым списком транзакций."""
        categories = ["Перевод организации"]
        result = count_transactions_by_category([], categories)
        assert result == {}

    def test_count_empty_categories(self) -> None:
        """Тестирует подсчет с пустым списком категорий."""
        transactions = [{"description": "Перевод организации"}]
        result = count_transactions_by_category(transactions, [])
        assert result == {}

    def test_count_missing_description(self) -> None:
        """Тестирует подсчет при отсутствии описания."""
        transactions = [
            {"id": 1},
            {"description": "Перевод организации"},
        ]
        categories = ["Перевод организации", "Перевод с карты на карту"]
        result = count_transactions_by_category(transactions, categories)
        assert result == {"Перевод организации": 1, "Перевод с карты на карту": 0}
