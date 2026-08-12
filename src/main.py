"""Главный модуль для запуска приложения."""

import json
from datetime import datetime

from src.views import events_page, main_page


def main() -> None:
    """Основная функция."""
    print("Банковский виджет - Курсовая работа")
    print("=" * 40)

    date_str = datetime.now().strftime("%Y-%m-%d")

    print("\n=== Главная страница ===")
    main_result = main_page(date_str)
    print(json.dumps(main_result, ensure_ascii=False, indent=2))

    print("\n=== Страница событий ===")
    events_result = events_page(date_str, "month")
    print(json.dumps(events_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
