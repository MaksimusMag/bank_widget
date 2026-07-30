"""Фикстуры для тестов банковского виджета."""

from typing import Dict, List

import pytest


@pytest.fixture
def sample_transactions() -> List[Dict[str, str]]:
    """Фикстура с тестовыми транзакциями для всех тестов."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def transactions_with_same_dates() -> List[Dict[str, str]]:
    """Фикстура с транзакциями, имеющими одинаковые даты."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T10:00:00.000000"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-01T10:00:00.000000"},
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, str]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def transactions_with_missing_dates() -> List[Dict[str, str]]:
    """Фикстура с транзакциями, у которых отсутствует дата."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": ""},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-31T23:59:59.999999"},
    ]


@pytest.fixture
def invalid_date_transactions() -> List[Dict[str, str]]:
    """Фикстура с транзакциями, имеющими нестандартные форматы дат."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "01.01.2024"},
        {"id": 2, "state": "EXECUTED", "date": "2024/01/01"},
        {"id": 3, "state": "EXECUTED", "date": "invalid-date"},
    ]


@pytest.fixture
def sample_transactions_simple() -> list:
    """Простая фикстура с транзакциями для тестов сортировки."""
    return [
        {"id": 1, "date": "2024-01-03T00:00:00.000000"},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]


@pytest.fixture
def sample_transactions_with_currency() -> List[Dict]:
    """Фикстура с транзакциями, содержащими информацию о валюте."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def empty_transactions_list() -> List[Dict]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def transactions_without_currency() -> List[Dict]:
    """Фикстура с транзакциями, у которых отсутствует валюта."""
    return [
        {"id": 1, "description": "Транзакция без валюты", "operationAmount": {}},
        {
            "id": 2,
            "description": "Транзакция без поля currency",
        },
    ]


@pytest.fixture
def card_range_params() -> List[tuple]:
    """Фикстура с параметрами для тестирования генератора номеров карт."""
    return [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999999999999990,
            9999999999999995,
            [
                "9999 9999 9999 9990",
                "9999 9999 9999 9991",
                "9999 9999 9999 9992",
                "9999 9999 9999 9993",
                "9999 9999 9999 9994",
                "9999 9999 9999 9995",
            ],
        ),
        (1, 1, ["0000 0000 0000 0001"]),
    ]
