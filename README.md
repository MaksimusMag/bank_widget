# Bank Widget

Виджет для отображения и обработки банковских операций клиента.

## Описание проекта

Проект предоставляет набор функций для работы с банковскими операциями:
- Маскировка номеров карт и счетов
- Форматирование дат
- Чтение данных из CSV и Excel файлов

## Структура проекта
bank_widget/
├── .git/
├── .gitignore
├── .flake8
├── pyproject.toml
├── README.md
├── data/
├── src/
│ ├── init.py
│ ├── constants.py
│ ├── masks.py
│ ├── reading.py
│ └── widget.py
└── tests/
├── init.py
├── test_masks.py
├── test_reading.py
└── test_widget.py

text

## Установка

```bash
git clone https://github.com/MaksimusMag/bank_widget.git
cd bank_widget
poetry install
poetry shell
Использование
Чтение CSV-файла
python
from src import read_transactions_from_csv

transactions = read_transactions_from_csv("data/transactions.csv")
print(len(transactions))
Чтение Excel-файла
python
from src import read_transactions_from_excel

transactions = read_transactions_from_excel("data/transactions.xlsx")
print(len(transactions))
Маскировка номеров
python
from src import mask_account_card, get_date

result = mask_account_card("Visa Platinum 7000792289606361")
print(result)  # Visa Platinum 7000 79** **** 6361
Тестирование
bash
poetry run pytest tests/ -v
poetry run pytest tests/ -v --cov=src/ --cov-report=term
Лицензия
MIT
