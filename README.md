# Bank Widget

Виджет для отображения и обработки банковских операций клиента.

## Описание проекта

Проект предоставляет набор функций для работы с банковскими операциями:
- Маскировка номеров карт и счетов
- Форматирование дат
- Фильтрация и сортировка транзакций
- Генерация и обработка данных транзакций

## Структура проекта
bank_widget/
├── .git/
├── .gitignore
├── .flake8
├── pyproject.toml
├── poetry.lock (игнорируется)
├── README.md
├── htmlcov/ (отчет о покрытии)
├── src/
│ ├── init.py
│ ├── constants.py # Константы проекта
│ ├── generators.py # Генераторы для работы с данными
│ ├── masks.py # Маскировка номеров
│ ├── widget.py # Основной виджет
│ └── processing.py # Обработка данных
└── tests/
├── init.py
├── conftest.py # Фикстуры для тестов
├── test_masks.py
├── test_widget.py
├── test_processing.py
└── test_generators.py

text

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/MaksimusMag/bank_widget.git
cd bank_widget
Установите Poetry (если не установлен):

bash
curl -sSL https://install.python-poetry.org | python3 -
Установите зависимости:

bash
poetry install --with lint
Активируйте виртуальное окружение:

bash
poetry shell
Использование
Маскировка номеров
python
from src import mask_account_card, get_date

# Маскировка карты
result = mask_account_card("Visa Platinum 7000792289606361")
print(result)  # Visa Platinum 7000 79** **** 6361

# Маскировка счета
result = mask_account_card("Счет 73654108430135874305")
print(result)  # Счет **4305

# Форматирование даты
result = get_date("2024-03-11T02:26:18.671407")
print(result)  # 11.03.2024
Фильтрация и сортировка транзакций
python
from src import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Фильтрация по статусу
executed = filter_by_state(transactions)  # только EXECUTED
canceled = filter_by_state(transactions, 'CANCELED')  # только CANCELED

# Сортировка по дате
sorted_desc = sort_by_date(transactions)  # по убыванию (сначала новые)
sorted_asc = sort_by_date(transactions, ascending_order=True)  # по возрастанию
Использование констант
Проект использует централизованные константы из модуля src.constants.py:

python
from src import (
    EXECUTED_STATUS,
    CANCELED_STATUS,
    PENDING_STATUS,
    CARD_NUMBER_LENGTH,
    ACCOUNT_NUMBER_MIN_LENGTH
)

print(f"Длина номера карты: {CARD_NUMBER_LENGTH}")  # 16
print(f"Минимальная длина счета: {ACCOUNT_NUMBER_MIN_LENGTH}")  # 4
print(f"Статус выполнения: {EXECUTED_STATUS}")  # EXECUTED
Все магические числа вынесены в константы для улучшения читаемости и поддерживаемости кода.

Генераторы для работы с данными
Модуль generators.py предоставляет функции-генераторы для эффективной работы с данными транзакций.

filter_by_currency(transactions, currency_code)
Фильтрует транзакции по заданной валюте, возвращая итератор.

Параметры:

transactions (List[Dict]): Список транзакций

currency_code (str): Код валюты (например, "USD", "RUB")

Возвращает: Итератор с транзакциями в указанной валюте

Пример:

python
from src import filter_by_currency

transactions = [
    {
        "id": 939719570,
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации"
    },
    {
        "id": 873106923,
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод со счета на счет"
    }
]

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["operationAmount"]["amount"])
# 9824.07
transaction_descriptions(transactions)
Генерирует описания транзакций по очереди.

Параметры:

transactions (List[Dict]): Список транзакций

Возвращает: Генератор строк с описаниями

Пример:

python
from src import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)
# Перевод организации
# Перевод со счета на счет
# Перевод со счета на счет
# Перевод с карты на карту
# Перевод организации
card_number_generator(start, stop)
Генерирует номера банковских карт в заданном диапазоне.

Параметры:

start (int): Начальное значение (включительно)

stop (int): Конечное значение (включительно)

Возвращает: Генератор номеров карт в формате XXXX XXXX XXXX XXXX

Пример:

python
from src import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
API Reference
Модуль masks.py
get_mask_card_number(card_number: str) -> str
Маскирует номер банковской карты.

Параметры:

card_number (str): Номер карты (16 цифр)

Возвращает: Замаскированный номер в формате XXXX XX** **** XXXX

Пример:

python
>>> get_mask_card_number("7000792289606361")
'7000 79** **** 6361'
get_mask_account(account_number: str) -> str
Маскирует номер банковского счета.

Параметры:

account_number (str): Номер счета

Возвращает: Замаскированный номер в формате **XXXX

Пример:

python
>>> get_mask_account("73654108430135874305")
'**4305'
Модуль widget.py
mask_account_card(account_card_info: str) -> str
Маскирует номер карты или счета в зависимости от типа.

Параметры:

account_card_info (str): Строка с типом и номером

Возвращает: Строка с замаскированным номером

Примеры:

python
>>> mask_account_card("Visa Platinum 7000792289606361")
'Visa Platinum 7000 79** **** 6361'

>>> mask_account_card("Счет 73654108430135874305")
'Счет **4305'
get_date(iso_date_string: str) -> str
Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

Параметры:

iso_date_string (str): Дата в формате YYYY-MM-DDTHH:MM:SS.ffffff

Возвращает: Дата в формате ДД.ММ.ГГГГ

Пример:

python
>>> get_date("2024-03-11T02:26:18.671407")
'11.03.2024'
Модуль processing.py
filter_by_state(transaction_data: TransactionList, target_state: str = EXECUTED_STATUS) -> TransactionList
Фильтрует список транзакций по значению ключа 'state'.

Параметры:

transaction_data (TransactionList): Список словарей с транзакциями

target_state (str): Значение для фильтрации. По умолчанию 'EXECUTED'

Возвращает: Новый список отфильтрованных транзакций

Пример:

python
>>> transactions = [
...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03...'},
...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12...'}
... ]
>>> filter_by_state(transactions)
[{'id': 41428829, 'state': 'EXECUTED', ...}]
sort_by_date(transaction_data: TransactionList, ascending_order: bool = False) -> TransactionList
Сортирует список транзакций по дате.

Параметры:

transaction_data (TransactionList): Список словарей с транзакциями

ascending_order (bool): Порядок сортировки. False - убывание, True - возрастание

Возвращает: Новый отсортированный список транзакций

Пример:

python
>>> sort_by_date(transactions)  # убывание
[{'id': 41428829, ...}, {'id': 594226727, ...}]
>>> sort_by_date(transactions, ascending_order=True)  # возрастание
[{'id': 594226727, ...}, {'id': 41428829, ...}]
Модуль generators.py
filter_by_currency(transactions: List[Dict], currency_code: str) -> Iterator[Dict]
Фильтрует транзакции по заданной валюте.

Параметры:

transactions (List[Dict]): Список транзакций

currency_code (str): Код валюты (например, "USD", "RUB")

Возвращает: Итератор с транзакциями в указанной валюте

Пример:

python
>>> usd_transactions = filter_by_currency(transactions, "USD")
>>> for transaction in usd_transactions:
...     print(transaction["operationAmount"]["currency"]["code"])
USD
USD
USD
transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]
Генерирует описания транзакций по очереди.

Параметры:

transactions (List[Dict]): Список транзакций

Возвращает: Генератор строк с описаниями

Пример:

python
>>> descriptions = transaction_descriptions(transactions)
>>> for desc in descriptions:
...     print(desc)
Перевод организации
Перевод со счета на счет
Перевод со счета на счет
card_number_generator(start: int, stop: int) -> Generator[str, None, None]
Генерирует номера банковских карт в заданном диапазоне.

Параметры:

start (int): Начальное значение (включительно)

stop (int): Конечное значение (включительно)

Возвращает: Генератор номеров карт в формате XXXX XXXX XXXX XXXX

Пример:

python
>>> for card in card_number_generator(1, 5):
...     print(card)
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
Тестирование
Структура тестов
Тесты организованы с использованием передовых практик pytest:

Фикстуры (conftest.py) - централизованное управление тестовыми данными:

sample_transactions - стандартный набор транзакций

sample_transactions_with_currency - транзакции с валютой

transactions_with_same_dates - транзакции с одинаковыми датами

transactions_with_missing_dates - транзакции без дат

invalid_date_transactions - транзакции с нестандартными форматами дат

empty_transactions - пустой список

card_range_params - параметры для тестирования номеров карт

Параметризация - тестирование различных сценариев без дублирования кода:

Различные форматы номеров карт и счетов

Различные статусы транзакций (EXECUTED, CANCELED, PENDING)

Различные валюты (USD, RUB, EUR)

Различные диапазоны номеров карт

Граничные случаи и некорректные входные данные

Запуск тестов
bash
# Запустить все тесты
poetry run pytest tests/ -v

# Запустить тесты конкретного модуля
poetry run pytest tests/test_processing.py -v
poetry run pytest tests/test_generators.py -v

# Запустить с отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=term

# Запустить с HTML отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=html
Покрытие кода
На данный момент покрытие кода составляет 100%:

Модуль	Покрытие
src/__init__.py	100%
src/constants.py	100%
src/generators.py	100%
src/masks.py	100%
src/widget.py	100%
src/processing.py	100%
ИТОГО	100%
Все функции и ветви кода покрыты тестами, включая:

Валидные и невалидные входные данные

Граничные случаи

Обработку исключений

Различные статусы и форматы данных

Различные валюты и диапазоны номеров

Проверка качества кода
bash
# Проверка форматирования
poetry run black --check src/ tests/

# Автоформатирование
poetry run black src/ tests/

# Проверка сортировки импортов
poetry run isort --check-only src/ tests/

# Сортировка импортов
poetry run isort src/ tests/

# Проверка стиля
poetry run flake8 src/ tests/

# Проверка типов
poetry run mypy src/
Технологии
Python 3.10+ - язык программирования

Poetry - управление зависимостями

pytest - фреймворк для тестирования

pytest-cov - измерение покрытия кода

Black - форматирование кода

isort - сортировка импортов

flake8 - проверка стиля

mypy - проверка типов

Требования к коду
Проект следует стандартам PEP 8:

Использование snake_case для имен переменных и функций

Максимальная длина строки: 100 символов

Использование type hints для всех функций

Документирование всех публичных функций (docstrings)

Покрытие тестами не менее 80%

Автор
Максим Обросков

Лицензия
MIT
