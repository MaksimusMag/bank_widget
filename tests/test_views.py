"""Тесты для модуля views."""

from unittest.mock import patch

import pandas as pd

from src.views import (
    events_page,
    get_card_info,
    get_currency_rates,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
    main_page,
)


class TestGetGreeting:
    """Тесты для функции get_greeting."""

    @patch("src.views.datetime")
    def test_greeting_morning(self, mock_datetime) -> None:
        """Тестирует приветствие для утра."""
        mock_datetime.now.return_value.hour = 8
        assert get_greeting() == "Доброе утро"

    @patch("src.views.datetime")
    def test_greeting_afternoon(self, mock_datetime) -> None:
        """Тестирует приветствие для дня."""
        mock_datetime.now.return_value.hour = 14
        assert get_greeting() == "Добрый день"

    @patch("src.views.datetime")
    def test_greeting_evening(self, mock_datetime) -> None:
        """Тестирует приветствие для вечера."""
        mock_datetime.now.return_value.hour = 20
        assert get_greeting() == "Добрый вечер"

    @patch("src.views.datetime")
    def test_greeting_night(self, mock_datetime) -> None:
        """Тестирует приветствие для ночи."""
        mock_datetime.now.return_value.hour = 2
        assert get_greeting() == "Доброй ночи"


class TestGetCardInfo:
    """Тесты для функции get_card_info."""

    def test_get_card_info_empty(self) -> None:
        """Тестирует пустой датафрейм."""
        df = pd.DataFrame()
        result = get_card_info(df)
        assert result == []

    def test_get_card_info_valid(self) -> None:
        """Тестирует получение информации по картам."""
        data = {
            "Номер карты": ["1234", "1234", "5678"],
            "Сумма платежа": [100, 200, 50],
            "Кешбэк": [1, 2, 0.5],
        }
        df = pd.DataFrame(data)
        result = get_card_info(df)

        assert len(result) == 2
        assert result[0]["last_digits"] == "1234"
        assert result[0]["total_spent"] == 300
        assert result[0]["cashback"] == 3


class TestGetTopTransactions:
    """Тесты для функции get_top_transactions."""

    def test_get_top_transactions_valid(self) -> None:
        """Тестирует получение топ-N транзакций."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20", "2024-01-21"],
            "Сумма платежа": [100, 50, 200],
            "Категория": ["Еда", "Транспорт", "Супермаркеты"],
            "Описание": ["Покупка 1", "Такси", "Продукты"],
        }
        df = pd.DataFrame(data)
        result = get_top_transactions(df, 2)
        assert len(result) == 2
        assert result[0]["amount"] == 200
        assert result[1]["amount"] == 100

    def test_get_top_transactions_empty(self) -> None:
        """Тестирует пустой датафрейм."""
        df = pd.DataFrame()
        result = get_top_transactions(df)
        assert result == []


class TestGetCurrencyRates:
    """Тесты для функции get_currency_rates."""

    def test_get_currency_rates_valid(self) -> None:
        """Тестирует получение курсов валют."""
        result = get_currency_rates(["USD", "EUR"])
        assert len(result) == 2
        assert result[0]["currency"] == "USD"
        assert result[0]["rate"] > 0


class TestGetStockPrices:
    """Тесты для функции get_stock_prices."""

    def test_get_stock_prices_valid(self) -> None:
        """Тестирует получение цен акций."""
        result = get_stock_prices(["AAPL", "AMZN"])
        assert len(result) == 2
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] > 0


class TestEventsPage:
    """Тесты для функции events_page."""

    @patch("src.views.pd.read_excel")
    def test_events_page_valid(self, mock_read_excel) -> None:
        """Тестирует страницу событий."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20"],
            "Сумма платежа": [100, 200],
        }
        mock_df = pd.DataFrame(data)
        mock_read_excel.return_value = mock_df

        result = events_page("2024-01-20", "month")
        assert "expenses" in result
        assert "income" in result
        assert "currency_rates" in result
        assert "stock_prices" in result

    @patch("src.views.pd.read_excel")
    def test_events_page_empty(self, mock_read_excel) -> None:
        """Тестирует страницу событий с пустыми данными."""
        mock_read_excel.return_value = pd.DataFrame()
        result = events_page("2024-01-20")
        assert result == {"error": "No data available"}


class TestMainPage:
    """Тесты для функции main_page."""

    @patch("src.views.pd.read_excel")
    def test_main_page_valid(self, mock_read_excel) -> None:
        """Тестирует главную страницу."""
        data = {
            "Дата операции": ["2024-01-15", "2024-01-20"],
            "Номер карты": ["1234", "5678"],
            "Сумма платежа": [100, 200],
            "Категория": ["Еда", "Транспорт"],
            "Описание": ["Покупка", "Такси"],
            "Кешбэк": [1, 2],
        }
        mock_df = pd.DataFrame(data)
        mock_read_excel.return_value = mock_df

        result = main_page("2024-01-20")
        assert "greeting" in result
        assert "cards" in result
        assert "top_transactions" in result
        assert "currency_rates" in result
        assert "stock_prices" in result

    @patch("src.views.pd.read_excel")
    def test_main_page_empty(self, mock_read_excel) -> None:
        """Тестирует главную страницу с пустыми данными."""
        mock_read_excel.return_value = pd.DataFrame()
        result = main_page("2024-01-20")
        assert result == {"error": "No data available"}
