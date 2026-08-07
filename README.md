# Bank Widget

Виджет для отображения и обработки банковских операций клиента.

## Описание проекта

Проект предоставляет набор функций для работы с банковскими операциями:
- Маскировка номеров карт и счетов
- Форматирование дат
- Фильтрация и сортировка транзакций
- Логирование выполнения функций
- Работа с JSON-файлами

## Структура проекта
bank_widget/
├── .git/
├── .gitignore
├── .flake8
├── pyproject.toml
├── poetry.lock (игнорируется)
├── README.md
├── logs/
│ ├── masks.log # Логи модуля masks
│ └── utils.log # Логи модуля utils
├── src/
│ ├── init.py
│ ├── constants.py # Константы проекта
│ ├── masks.py # Маскировка номеров (с логированием)
│ ├── utils.py # Утилиты (с логированием)
│ └── widget.py # Основной виджет
└── tests/
├── init.py
├── test_masks.py
├── test_utils.py
└── test_widget.py

## Установка

1. Клонируйте репозиторий:

git clone https://github.com/MaksimusMag/bank_widget.git
cd bank_widget
Установите Poetry (если не установлен):


curl -sSL https://install.python-poetry.org | python3 -
Установите зависимости:


poetry install
Активируйте виртуальное окружение:

poetry shell
Использование
Маскировка номеров

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
Работа с JSON-файлами

from src import read_transactions_from_json

transactions = read_transactions_from_json("data/operations.json")
print(len(transactions))  # Количество транзакций
Использование констант

from src import (
    EXECUTED_STATUS,
    CANCELED_STATUS,
    CARD_NUMBER_LENGTH,
    ACCOUNT_NUMBER_MIN_LENGTH
)

print(f"Длина номера карты: {CARD_NUMBER_LENGTH}")  # 16
print(f"Минимальная длина счета: {ACCOUNT_NUMBER_MIN_LENGTH}")  # 4
Логирование
Проект использует библиотеку logging для записи логов.

Модуль masks.py
Логи записываются в файл logs/masks.log:

Уровень: DEBUG и выше

Формат: %(asctime)s - %(name)s - %(levelname)s - %(message)s

Пример: 2026-08-07 12:00:00 - src.masks - INFO - get_mask_card_number: успешно замаскирован номер 7000...

Модуль utils.py
Логи записываются в файл logs/utils.log:

Уровень: DEBUG и выше

Формат: %(asctime)s - %(name)s - %(levelname)s - %(message)s

Пример: 2026-08-07 12:00:00 - src.utils - INFO - Успешно прочитано 6 транзакций из data/operations.json

API Reference
Модуль masks.py
get_mask_card_number(card_number: str) -> str — маскирует номер карты

get_mask_account(account_number: str) -> str — маскирует номер счета

Модуль widget.py
mask_account_card(account_card_info: str) -> str — маскирует карту или счет

get_date(date_string: str) -> str — преобразует дату в формат ДД.ММ.ГГГГ

Модуль utils.py
read_transactions_from_json(file_path: str) -> List[Dict[str, Any]] — чтение JSON-файла

Тестирование
Запуск тестов

# Запустить все тесты
poetry run pytest tests/ -v

# Запустить с отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=term

# Запустить с HTML отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=html
Покрытие кода
На данный момент покрытие кода составляет 91%:

Модуль	Покрытие
src/__init__.py	100%
src/constants.py	100%
src/masks.py	98%
src/utils.py	88%
src/widget.py	79%
ИТОГО	91%
Проверка качества кода

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
Python 3.10+ — язык программирования

Poetry — управление зависимостями

pytest — фреймворк для тестирования

pytest-cov — измерение покрытия кода

Black — форматирование кода

isort — сортировка импортов

flake8 — проверка стиля

mypy — проверка типов

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