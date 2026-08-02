"""Тесты для модуля external_api."""

import os
from unittest.mock import Mock, patch

import requests

from src.external_api import convert_to_rubles


class TestConvertToRubles:
    """Тесты для функции convert_to_rubles."""

    def test_convert_rub_to_rub(self) -> None:
        """Тестирует конвертацию RUB в RUB (без изменений)."""
        transaction = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}
        result = convert_to_rubles(transaction)
        assert result == 1000.50

    def test_convert_usd_to_rub_success(self) -> None:
        """Тестирует успешную конвертацию USD в RUB."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 9000.0}
        mock_response.raise_for_status = Mock()

        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        with patch("src.external_api.requests.get", return_value=mock_response):
            with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}):
                result = convert_to_rubles(transaction)
                assert result == 9000.0

    def test_convert_eur_to_rub_success(self) -> None:
        """Тестирует успешную конвертацию EUR в RUB."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 9500.0}
        mock_response.raise_for_status = Mock()

        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "EUR"}}}

        with patch("src.external_api.requests.get", return_value=mock_response):
            with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}):
                result = convert_to_rubles(transaction)
                assert result == 9500.0

    def test_convert_without_api_key(self) -> None:
        """Тестирует конвертацию без API ключа."""
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        with patch.dict(os.environ, {}, clear=True):
            result = convert_to_rubles(transaction)
            assert result == 100.0

    def test_convert_api_error(self) -> None:
        """Тестирует обработку ошибки API."""
        with patch("src.external_api.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("API Error")

            transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

            with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}):
                result = convert_to_rubles(transaction)
                assert result == 100.0

    def test_convert_api_invalid_response(self) -> None:
        """Тестирует обработку некорректного ответа API."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": False}
        mock_response.raise_for_status = Mock()

        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        with patch("src.external_api.requests.get", return_value=mock_response):
            with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}):
                result = convert_to_rubles(transaction)
                assert result == 100.0

    def test_convert_missing_amount(self) -> None:
        """Тестирует обработку отсутствия суммы в транзакции."""
        transaction = {"operationAmount": {"currency": {"code": "USD"}}}
        result = convert_to_rubles(transaction)
        assert result == 0.0

    def test_convert_invalid_amount(self) -> None:
        """Тестирует обработку некорректной суммы."""
        transaction = {"operationAmount": {"amount": "invalid", "currency": {"code": "USD"}}}
        result = convert_to_rubles(transaction)
        assert result == 0.0

    def test_convert_unknown_currency(self) -> None:
        """Тестирует конвертацию неизвестной валюты."""
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "GBP"}}}
        result = convert_to_rubles(transaction)
        assert result == 100.0

    @patch("src.external_api.requests.get")
    def test_convert_timeout(self, mock_get) -> None:
        """Тестирует обработку таймаута API."""
        mock_get.side_effect = requests.exceptions.Timeout()

        transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}):
            result = convert_to_rubles(transaction)
            assert result == 100.0
