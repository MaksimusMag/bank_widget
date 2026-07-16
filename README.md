# Bank Widget

Виджет для отображения и обработки банковских операций клиента.

## Описание проекта

Проект предоставляет набор функций для работы с банковскими операциями:
- Маскировка номеров карт и счетов
- Форматирование дат
- Фильтрация и сортировка транзакций

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш_логин/bank_widget.git
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
Фильтрация и сортировка
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
sorted_asc = sort_by_date(transactions, ascending=True)  # по возрастанию
Запуск тестов
bash
poetry run pytest tests/ -v
Проверка качества кода
bash
# Проверка форматирования
poetry run black --check src/ tests/

# Проверка сортировки импортов
poetry run isort --check-only src/ tests/

# Проверка стиля
poetry run flake8 src/ tests/

# Проверка типов
poetry run mypy src/
Технологии
Python 3.10+

Poetry - управление зависимостями

pytest - тестирование

Black, isort, flake8, mypy - качество кода

Автор
Максим Обросков

Лицензия
MIT