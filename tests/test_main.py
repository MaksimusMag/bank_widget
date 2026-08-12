"""Тесты для модуля main."""

from unittest.mock import patch

from src.main import main


@patch("src.main.main_page")
@patch("src.main.events_page")
def test_main(mock_events_page, mock_main_page) -> None:
    """Тестирует функцию main."""
    mock_main_page.return_value = {"greeting": "Добрый день"}
    mock_events_page.return_value = {"expenses": {"total_amount": 0}}

    with patch("src.main.datetime") as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "2024-01-20"
        main()

    mock_main_page.assert_called_once_with("2024-01-20")
    mock_events_page.assert_called_once_with("2024-01-20", "month")
