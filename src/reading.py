"""Модуль для чтения данных из CSV и Excel файлов."""

import csv
from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла."""
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data: List[Dict[str, Any]] = list(reader)

            if not data:
                return []

            return data

    except (FileNotFoundError, ValueError, csv.Error):
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла."""
    try:
        df = pd.read_excel(file_path, engine="openpyxl")

        if df.empty:
            return []

        data: List[Dict[str, Any]] = df.to_dict(orient="records")

        return data

    except (FileNotFoundError, ValueError, Exception):
        return []
