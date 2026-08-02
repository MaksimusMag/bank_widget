"""Тесты для модуля decorators."""

import os

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log."""

    @log()
    def add(self, a: int, b: int) -> int:
        return a + b

    def test_log_console_success(self, capsys) -> None:
        """Тестирует логирование успешного выполнения в консоль."""
        result = self.add(2, 3)
        assert result == 5

        captured = capsys.readouterr()
        assert "add ok" in captured.err

    def test_log_console_error(self, capsys) -> None:
        """Тестирует логирование ошибки в консоль."""

        @log()
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.err

    def test_log_file_success(self) -> None:
        """Тестирует логирование успешного выполнения в файл."""
        test_file = "test_log.txt"

        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except PermissionError:
                pass

        @log(filename=test_file)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 5)
        assert result == 20

        assert os.path.exists(test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "multiply ok" in content

        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except PermissionError:
                pass
