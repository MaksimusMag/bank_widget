"""Тесты для модуля processing."""

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default():
    """Тестирует фильтрацию по умолчанию (EXECUTED)."""
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(transactions)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)
    assert result[0]['id'] == 41428829
    assert result[1]['id'] == 939719570


def test_filter_by_state_canceled():
    """Тестирует фильтрацию по статусу CANCELED."""
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = filter_by_state(transactions, 'CANCELED')
    assert len(result) == 2
    assert all(item['state'] == 'CANCELED' for item in result)
    assert result[0]['id'] == 594226727
    assert result[1]['id'] == 615064591


def test_filter_by_state_empty():
    """Тестирует фильтрацию пустого списка."""
    assert filter_by_state([]) == []


def test_filter_by_state_invalid_state():
    """Тестирует фильтрацию с несуществующим статусом."""
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]
    result = filter_by_state(transactions, 'PENDING')
    assert result == []


def test_sort_by_date_descending():
    """Тестирует сортировку по убыванию (по умолчанию)."""
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = sort_by_date(transactions)
    assert len(result) == 4
    # Проверяем, что даты отсортированы по убыванию
    dates = [item['date'] for item in result]
    assert dates == sorted(dates, reverse=True)
    # Проверяем конкретный порядок
    assert result[0]['id'] == 41428829  # 2019-07-03
    assert result[1]['id'] == 615064591  # 2018-10-14
    assert result[2]['id'] == 594226727  # 2018-09-12
    assert result[3]['id'] == 939719570  # 2018-06-30


def test_sort_by_date_ascending():
    """Тестирует сортировку по возрастанию."""
    transactions = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    result = sort_by_date(transactions, ascending=True)
    assert len(result) == 4
    # Проверяем, что даты отсортированы по возрастанию
    dates = [item['date'] for item in result]
    assert dates == sorted(dates)
    # Проверяем конкретный порядок
    assert result[0]['id'] == 939719570  # 2018-06-30
    assert result[1]['id'] == 594226727  # 2018-09-12
    assert result[2]['id'] == 615064591  # 2018-10-14
    assert result[3]['id'] == 41428829  # 2019-07-03


def test_sort_by_date_empty():
    """Тестирует сортировку пустого списка."""
    assert sort_by_date([]) == []


def test_sort_by_date_missing_date():
    """Тестирует сортировку, когда у некоторых записей отсутствует дата."""
    transactions = [
        {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01'},
        {'id': 2, 'state': 'EXECUTED'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2019-01-01'}
    ]
    result = sort_by_date(transactions)
    # Записи без даты должны быть в конце
    assert len(result) == 3
    assert result[0]['id'] == 1  # 2020-01-01
    assert result[1]['id'] == 3  # 2019-01-01
    assert result[2]['id'] == 2  # нет даты