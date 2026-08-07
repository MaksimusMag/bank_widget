"""Тесты для модуля utils."""

import json
import os
import tempfile

from src.utils import read_transactions_from_json


class TestReadTransactionsFromJson:
    """Тесты для функции read_transactions_from_json."""

    def test_read_valid_json(self) -> None:
        """Тестирует чтение валидного JSON-файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump([{"id": 1, "amount": 100}], tmp)
            tmp_path = tmp.name

        try:
            result = read_transactions_from_json(tmp_path)
            assert len(result) == 1
            assert result[0]["id"] == 1
            assert result[0]["amount"] == 100
        finally:
            os.remove(tmp_path)

    def test_read_empty_file(self) -> None:
        """Тестирует чтение пустого файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("")
            tmp_path = tmp.name

        try:
            result = read_transactions_from_json(tmp_path)
            assert result == []
        finally:
            os.remove(tmp_path)

    def test_read_non_list_json(self) -> None:
        """Тестирует чтение JSON, который не является списком."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump({"key": "value"}, tmp)
            tmp_path = tmp.name

        try:
            result = read_transactions_from_json(tmp_path)
            assert result == []
        finally:
            os.remove(tmp_path)

    def test_read_invalid_json(self) -> None:
        """Тестирует чтение некорректного JSON."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("invalid json content")
            tmp_path = tmp.name

        try:
            result = read_transactions_from_json(tmp_path)
            assert result == []
        finally:
            os.remove(tmp_path)

    def test_file_not_found(self) -> None:
        """Тестирует чтение несуществующего файла."""
        result = read_transactions_from_json("non_existent_file.json")
        assert result == []

    def test_read_file_with_empty_list(self) -> None:
        """Тестирует чтение файла с пустым списком."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump([], tmp)
            tmp_path = tmp.name

        try:
            result = read_transactions_from_json(tmp_path)
            assert result == []
        finally:
            os.remove(tmp_path)
