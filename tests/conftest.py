"""Фикстуры для тестов банковского виджета."""

from typing import Dict, List, Union

import pytest


@pytest.fixture
def sample_transactions() -> List[Dict[str, Union[str, int]]]:
    """
    Фикстура с тестовыми транзакциями для всех тестов.
    """
    return [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689"
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441"
        }
    ]


@pytest.fixture
def transactions_with_same_dates() -> List[Dict[str, Union[str, int]]]:
    """
    Фикстура с транзакциями, имеющими одинаковые даты.
    """
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-01T10:00:00.000000"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-01-01T10:00:00.000000"
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2024-01-01T10:00:00.000000"
        }
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Union[str, int]]]:
    """
    Фикстура с пустым списком транзакций.
    """
    return []


@pytest.fixture
def transactions_with_missing_dates() -> List[Dict[str, Union[str, int]]]:
    """
    Фикстура с транзакциями, у которых отсутствует дата.
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": ""},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-31T23:59:59.999999"}
    ]


@pytest.fixture
def invalid_date_transactions() -> List[Dict[str, Union[str, int]]]:
    """
    Фикстура с транзакциями, имеющими нестандартные форматы дат.
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "01.01.2024"},
        {"id": 2, "state": "EXECUTED", "date": "2024/01/01"},
        {"id": 3, "state": "EXECUTED", "date": "invalid-date"}
    ]


@pytest.fixture
def card_numbers() -> List[tuple]:
    """
    Фикстура с тестовыми номерами карт и ожидаемыми результатами.
    """
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]


@pytest.fixture
def account_numbers() -> List[tuple]:
    """
    Фикстура с тестовыми номерами счетов и ожидаемыми результатами.
    """
    return [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("11111111111111111111", "**1111"),
        ("000000000000", "**0000"),
    ]


@pytest.fixture
def card_info_data() -> List[tuple]:
    """
    Фикстура с тестовыми данными для mask_account_card.
    """
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ]


@pytest.fixture
def invalid_card_info() -> List[tuple]:
    """
    Фикстура с некорректными данными для mask_account_card.
    """
    return [
        ("", ""),
        ("Visa", "Visa"),
        ("Счет", "Счет"),
        ("Card 123", "Card 123"),
        ("Visa Platinum 123", "Visa Platinum 123"),
    ]


@pytest.fixture
def date_strings() -> List[tuple]:
    """
    Фикстура с тестовыми датами и ожидаемыми результатами.
    """
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-25T15:30:45.123456", "25.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
        ("2024-12-31T23:59:59.999999", "31.12.2024"),
        ("2024-06-15T12:00:00.000000", "15.06.2024"),
    ]


@pytest.fixture
def invalid_date_strings() -> List[tuple]:
    """
    Фикстура с некорректными датами.
    """
    return [
        ("", ""),
        ("invalid-date", "invalid-date"),
        ("2024/03/11T02:26:18", "2024/03/11T02:26:18"),
        ("2024-03-11", "2024-03-11"),
        ("T02:26:18.671407", "T02:26:18.671407"),
    ]
