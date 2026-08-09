"""Главный модуль для работы с банковскими транзакциями."""

from typing import Any, Dict, List

from src import (
    filter_rub_transactions,
    filter_transactions_by_state,
    read_transactions_from_csv,
    read_transactions_from_excel,
    read_transactions_from_json,
    search_transactions,
    sort_transactions_by_date,
)
from src.widget import get_date, mask_account_card


def main() -> None:
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # 1. Выбор источника данных
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nВаш выбор: ")

    transactions: List[Dict[str, Any]] = []

    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = read_transactions_from_json(file_path)
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = read_transactions_from_csv(file_path)
    elif choice == "3":
        print("\nДля обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = read_transactions_from_excel(file_path)
    else:
        print("Неверный выбор.")
        return

    if not transactions:
        print("Не найдено ни одной транзакции.")
        return

    # 2. Фильтрация по статусу
    filtered_transactions: List[Dict[str, Any]] = []

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        state = input("Статус: ").strip()

        if state.upper() not in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f'Статус операции "{state}" недоступен.')
            continue

        filtered_transactions = filter_transactions_by_state(transactions, state)
        print(f'Операции отфильтрованы по статусу "{state.upper()}"')
        break

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # 3. Сортировка по дате
    print("\nОтсортировать операции по дате? Да/Нет")
    sort_choice = input("Ваш выбор: ").strip().lower()

    if sort_choice in ["да", "д", "yes", "y"]:
        print("\nОтсортировать по возрастанию или по убыванию?")
        order = input("Ваш выбор: ").strip().lower()
        ascending = order in ["по возрастанию", "возрастанию", "asc"]
        filtered_transactions = sort_transactions_by_date(filtered_transactions, ascending)

    # 4. Фильтрация рублевых транзакций
    print("\nВыводить только рублевые транзакции? Да/Нет")
    rub_choice = input("Ваш выбор: ").strip().lower()

    if rub_choice in ["да", "д", "yes", "y"]:
        filtered_transactions = filter_rub_transactions(filtered_transactions)
        if not filtered_transactions:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return

    # 5. Поиск по описанию
    print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_choice = input("Ваш выбор: ").strip().lower()

    if search_choice in ["да", "д", "yes", "y"]:
        search_query = input("Введите слово для поиска: ").strip()
        filtered_transactions = search_transactions(filtered_transactions, search_query)
        if not filtered_transactions:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return

    # 6. Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        # Форматируем дату
        date_str = transaction.get("date", "")
        if date_str:
            try:
                date_str = get_date(date_str)
            except (ValueError, IndexError):
                pass

        description = transaction.get("description", "Описание отсутствует")

        # Форматируем счет/карту
        from_account = transaction.get("from", "")
        to_account = transaction.get("to", "")

        if from_account:
            from_account = mask_account_card(from_account)
        if to_account:
            to_account = mask_account_card(to_account)

        # Форматируем сумму
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("code", "")

        print(f"\n{date_str} {description}")
        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif to_account:
            print(f"Счет {to_account}")
        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
