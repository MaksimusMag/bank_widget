# Bank Widget

Виджет для отображения и обработки банковских операций клиента.

## Описание проекта

Проект предоставляет набор функций для работы с банковскими операциями:
- Маскировка номеров карт и счетов
- Форматирование дат
- Фильтрация и сортировка транзакций
- Генерация и обработка данных транзакций
- Логирование выполнения функций
- Работа с JSON-файлами
- Конвертация валют

## Структура проекта
bank_widget/
├── .git/
├── .gitignore
├── .flake8
├── pyproject.toml
├── poetry.lock (игнорируется)
├── README.md
├── .env.example # Шаблон для переменных окружения
├── .env # Переменные окружения (не в Git)
├── htmlcov/ # Отчет о покрытии
├── data/
│ └── operations.json # Данные о транзакциях
├── src/
│ ├── init.py
│ ├── constants.py # Константы проекта
│ ├── decorators.py # Декораторы для логирования
│ ├── external_api.py # Работа с внешними API
│ ├── generators.py # Генераторы для работы с данными
│ ├── masks.py # Маскировка номеров
│ ├── processing.py # Обработка данных
│ ├── utils.py # Утилиты для работы с данными
│ └── widget.py # Основной виджет
└── tests/
├── init.py
├── conftest.py # Фикстуры для тестов
├── test_decorators.py
├── test_external_api.py
├── test_generators.py
├── test_masks.py
├── test_processing.py
├── test_utils.py
└── test_widget.py

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
poetry install
Активируйте виртуальное окружение:

bash
poetry shell
Настройте переменные окружения:

bash
# Скопируйте шаблон .env.example в .env
cp .env.example .env
# Отредактируйте .env и добавьте свой API ключ
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
Генераторы для работы с данными
filter_by_currency(transactions, currency_code)
Фильтрует транзакции по заданной валюте, возвращая итератор.

python
from src import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["operationAmount"]["currency"]["code"])
# USD
# USD
# USD
transaction_descriptions(transactions)
Генерирует описания транзакций по очереди.

python
from src import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)
# Перевод организации
# Перевод со счета на счет
card_number_generator(start, stop)
Генерирует номера банковских карт в заданном диапазоне.

python
from src import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...
Декораторы
log(filename: Optional[str] = None)
Декоратор для логирования выполнения функций.

python
from src import log

# Логирование в файл
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)  # Запишет "my_function ok" в mylog.txt

# Логирование в консоль
@log()
def my_function(x, y):
    return x + y

my_function(1, 2)  # Выведет "my_function ok" в консоль
Работа с данными
read_transactions_from_json(file_path: str)
Читает данные о транзакциях из JSON-файла.

python
from src import read_transactions_from_json

transactions = read_transactions_from_json("data/operations.json")
print(len(transactions))  # 6
convert_to_rubles(transaction: Dict[str, Any]) -> float
Конвертирует сумму транзакции в рубли.

python
from src import convert_to_rubles

transaction = {
    "operationAmount": {
        "amount": "100",
        "currency": {"code": "USD"}
    }
}
rubles = convert_to_rubles(transaction)
print(rubles)  # ~9000.0
Настройка API ключа
Для работы конвертации валют необходимо настроить API ключ:

Получите ключ на https://apilayer.com/

Создайте файл .env на основе .env.example

Добавьте ключ в файл .env:

text
EXCHANGE_RATES_API_KEY=your_api_key_here
API Reference
Модуль masks.py
get_mask_card_number(card_number: str) -> str - маскирует номер карты

get_mask_account(account_number: str) -> str - маскирует номер счета

Модуль widget.py
mask_account_card(account_card_info: str) -> str - маскирует карту или счет

get_date(date_string: str) -> str - преобразует дату в формат ДД.ММ.ГГГГ

Модуль processing.py
filter_by_state(transaction_data, target_state) -> TransactionList - фильтрация по статусу

sort_by_date(transaction_data, ascending_order) -> TransactionList - сортировка по дате

Модуль generators.py
filter_by_currency(transactions, currency_code) -> Iterator[Dict] - фильтрация по валюте

transaction_descriptions(transactions) -> Generator[str, None, None] - генерация описаний

card_number_generator(start, stop) -> Generator[str, None, None] - генерация номеров карт

Модуль decorators.py
log(filename: Optional[str] = None) -> Callable - декоратор для логирования

Модуль utils.py
read_transactions_from_json(file_path: str) -> List[Dict[str, Any]] - чтение JSON-файла

Модуль external_api.py
convert_to_rubles(transaction: Dict[str, Any]) -> float - конвертация валют

Тестирование
Запуск тестов
bash
# Запустить все тесты
poetry run pytest tests/ -v

# Запустить с отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=term

# Запустить с HTML отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=html
Покрытие кода
На данный момент покрытие кода составляет 90%:

Модуль	Покрытие
src/__init__.py	100%
src/constants.py	100%
src/decorators.py	82%
src/external_api.py	100%
src/generators.py	79%
src/masks.py	95%
src/processing.py	100%
src/utils.py	100%
src/widget.py	81%
ИТОГО	90%
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

requests - HTTP-запросы к API

python-dotenv - управление переменными окружения

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