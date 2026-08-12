# Bank Widget

Виджет для отображения и обработки банковских операций клиента.

## Описание проекта

Проект предоставляет набор функций для работы с банковскими операциями:
- Маскировка номеров карт и счетов
- Форматирование дат
- Генерация JSON-ответов для веб-страниц (главная, события)
- Сервисы: Инвесткопилка, поиск, выгодные категории
- Отчеты: траты по категориям, по дням недели, в рабочие/выходные дни

## Структура проекта
bank_widget/
├── data/
│ └── operations.xls # Данные о транзакциях
├── reports/ # Папка для сохранения отчетов
├── src/
│ ├── init.py
│ ├── constants.py # Константы
│ ├── main.py # Главный модуль
│ ├── masks.py # Маскировка номеров
│ ├── reports.py # Отчеты
│ ├── services.py # Сервисы
│ ├── utils.py # Утилиты
│ ├── views.py # Веб-страницы
│ └── widget.py # Виджет
├── tests/
│ ├── init.py
│ ├── test_main.py
│ ├── test_masks.py
│ ├── test_reports.py
│ ├── test_services.py
│ ├── test_utils.py
│ ├── test_views.py
│ └── test_widget.py
├── user_settings.json # Настройки пользователя
├── .coveragerc
├── .env # Переменные окружения
├── .env_template # Шаблон .env
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md

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
Настройте переменные окружения:

# Скопируйте шаблон .env_template в .env
cp .env_template .env
# Отредактируйте .env и добавьте свои API ключи
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
Веб-страницы
Главная страница
Функция main_page(date_str) возвращает JSON-ответ с данными для главной страницы:

Приветствие в зависимости от времени суток

Информация по картам (последние 4 цифры, расходы, кешбэк)

Топ-5 транзакций по сумме

Курсы валют

Цены акций

from src.views import main_page

result = main_page("2024-01-20")
print(result)
Страница событий
Функция events_page(date_str, period) возвращает JSON-ответ с данными для страницы событий:

Расходы (общая сумма, основные категории, переводы и наличные)

Поступления (общая сумма, основные категории)

Курсы валют

Цены акций

Параметры:

date_str — дата в формате "YYYY-MM-DD"

period — период фильтрации ("month", "week", "year", "all")

from src.views import events_page

result = events_page("2024-01-20", "month")
print(result)
Сервисы
Инвесткопилка
Функция investment_bank(month, transactions, limit) рассчитывает сумму, которую можно отложить.

from src.services import investment_bank

transactions = [
    {"Дата операции": "2024-01-15", "Сумма операции": 1712},
]
result = investment_bank("2024-01", transactions, 50)
print(result)  # 38.0
Поиск
simple_search(transactions, query) — поиск по описанию или категории

search_by_phone(transactions) — поиск транзакций с телефонными номерами

search_transfers_to_individuals(transactions) — поиск переводов физическим лицам

from src.services import simple_search, search_by_phone

# Простой поиск
result = simple_search(transactions, "Перевод")

# Поиск по телефону
result = search_by_phone(transactions)
Выгодные категории
Функция profitable_categories(transactions, year, month) анализирует кешбэк по категориям.

from src.services import profitable_categories

result = profitable_categories(transactions, 2024, 1)
print(result)  # {"Супермаркеты": 25, "Транспорт": 5}
Отчеты
Траты по категории
Функция spending_by_category(transactions, category, date) возвращает траты по категории за последние 3 месяца.


from src.reports import spending_by_category

result = spending_by_category(df, "Супермаркеты", "2024-02-01")
Траты по дням недели
Функция spending_by_weekday(transactions, date) возвращает средние траты по дням недели.

from src.reports import spending_by_weekday

result = spending_by_weekday(df, "2024-02-01")
Траты в рабочие/выходные дни
Функция spending_by_workday(transactions, date) возвращает средние траты в рабочие и выходные дни.

from src.reports import spending_by_workday

result = spending_by_workday(df, "2024-02-01")
Тестирование
Запуск тестов

# Запустить все тесты
poetry run pytest tests/ -v

# Запустить с отчетом о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=term

# Сгенерировать HTML отчет о покрытии
poetry run pytest tests/ -v --cov=src/ --cov-report=html
Результаты тестирования
Параметр	Результат
Всего тестов	45
Пройдено	45 (100%)
Покрытие кода	94%
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

pandas — работа с данными

openpyxl — чтение Excel-файлов

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