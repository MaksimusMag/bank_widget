"""Тесты для модуля processing."""

from src.processing import filter_by_state, sort_by_date
from src.constants import EXECUTED_STATUS, CANCELED_STATUS


def test_filter_by_state_default() -> None:
    """Тестирует фильтрацию по умолчанию (EXECUTED)."""
    sample_transactions = [
        {'id': 41428829, 'state': EXECUTED_STATUS, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': EXECUTED_STATUS, 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': CANCELED_STATUS, 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': CANCELED_STATUS, 'date': '2018-10-14T08:21:33.419441'}
    ]

    filtered_result = filter_by_state(sample_transactions)
    expected_count = 2

    assert len(filtered_result) == expected_count
    assert all(transaction['state'] == EXECUTED_STATUS for transaction in filtered_result)
    assert filtered_result[0]['id'] == 41428829
    assert filtered_result[1]['id'] == 939719570


def test_filter_by_state_canceled() -> None:
    """Тестирует фильтрацию по статусу CANCELED."""
    sample_transactions = [
        {'id': 41428829, 'state': EXECUTED_STATUS, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': EXECUTED_STATUS, 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': CANCELED_STATUS, 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': CANCELED_STATUS, 'date': '2018-10-14T08:21:33.419441'}
    ]

    filtered_result = filter_by_state(sample_transactions, CANCELED_STATUS)
    expected_count = 2

    assert len(filtered_result) == expected_count
    assert all(transaction['state'] == CANCELED_STATUS for transaction in filtered_result)
    assert filtered_result[0]['id'] == 594226727
    assert filtered_result[1]['id'] == 615064591


def test_filter_by_state_empty() -> None:
    """Тестирует фильтрацию пустого списка."""
    empty_transactions = []
    filtered_result = filter_by_state(empty_transactions)
    assert filtered_result == []


def test_filter_by_state_invalid_state() -> None:
    """Тестирует фильтрацию с несуществующим статусом."""
    sample_transactions = [
        {'id': 41428829, 'state': EXECUTED_STATUS, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': EXECUTED_STATUS, 'date': '2018-06-30T02:08:58.425572'},
    ]
    invalid_state = "PENDING"
    filtered_result = filter_by_state(sample_transactions, invalid_state)
    assert filtered_result == []


def test_sort_by_date_descending() -> None:
    """Тестирует сортировку по убыванию (по умолчанию)."""
    sample_transactions = [
        {'id': 41428829, 'state': EXECUTED_STATUS, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': EXECUTED_STATUS, 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': CANCELED_STATUS, 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': CANCELED_STATUS, 'date': '2018-10-14T08:21:33.419441'}
    ]

    sorted_result = sort_by_date(sample_transactions)
    expected_count = 4

    assert len(sorted_result) == expected_count
    extracted_dates = [transaction['date'] for transaction in sorted_result]
    assert extracted_dates == sorted(extracted_dates, reverse=True)
    assert sorted_result[0]['id'] == 41428829
    assert sorted_result[1]['id'] == 615064591
    assert sorted_result[2]['id'] == 594226727
    assert sorted_result[3]['id'] == 939719570


def test_sort_by_date_ascending() -> None:
    """Тестирует сортировку по возрастанию."""
    sample_transactions = [
        {'id': 41428829, 'state': EXECUTED_STATUS, 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': EXECUTED_STATUS, 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': CANCELED_STATUS, 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': CANCELED_STATUS, 'date': '2018-10-14T08:21:33.419441'}
    ]

    sorted_result = sort_by_date(sample_transactions, ascending_order=True)
    expected_count = 4

    assert len(sorted_result) == expected_count
    extracted_dates = [transaction['date'] for transaction in sorted_result]
    assert extracted_dates == sorted(extracted_dates)
    assert sorted_result[0]['id'] == 939719570
    assert sorted_result[1]['id'] == 594226727
    assert sorted_result[2]['id'] == 615064591
    assert sorted_result[3]['id'] == 41428829


def test_sort_by_date_empty() -> None:
    """Тестирует сортировку пустого списка."""
    empty_transactions = []
    sorted_result = sort_by_date(empty_transactions)
    assert sorted_result == []


def test_sort_by_date_missing_date() -> None:
    """Тестирует сортировку, когда у некоторых записей отсутствует дата."""
    sample_transactions = [
        {'id': 1, 'state': EXECUTED_STATUS, 'date': '2020-01-01'},
        {'id': 2, 'state': EXECUTED_STATUS, 'date': ''},  # Транзакция без даты
        {'id': 3, 'state': EXECUTED_STATUS, 'date': '2019-01-01'}
    ]

    sorted_result = sort_by_date(sample_transactions)
    expected_count = 3

    assert len(sorted_result) == expected_count
    assert sorted_result[0]['id'] == 1  # Самая новая дата
    assert sorted_result[1]['id'] == 3  # Более старая дата
    assert sorted_result[2]['id'] == 2  # Без даты (пустая строка)
