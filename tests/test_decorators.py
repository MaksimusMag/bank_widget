"""Тесты для модуля decorators."""

import os
import shutil
import tempfile

import pytest

from src.decorators import log


# Тестовые функции
@log()
def add(a: int, b: int) -> int:
    """Тестовая функция сложения."""
    return a + b


@log()
def divide(a: int, b: int) -> float:
    """Тестовая функция деления."""
    return a / b


@log(filename="test_log.txt")
def multiply(a: int, b: int) -> int:
    """Тестовая функция умножения с логированием в файл."""
    return a * b


@log(filename="test_log.txt")
def failing_function(x: int) -> int:
    """Тестовая функция, которая всегда вызывает ошибку."""
    raise ValueError("Test error message")


@pytest.fixture
def temp_log_dir():
    """Фикстура для создания временной директории."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except PermissionError:
        pass


class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_console_success(self, capsys) -> None:
        """Тестирует логирование успешного выполнения в консоль."""
        result = add(2, 3)
        assert result == 5

        captured = capsys.readouterr()
        assert "add ok" in captured.err
        assert "INFO" in captured.err

    def test_log_console_error(self, capsys) -> None:
        """Тестирует логирование ошибки в консоль."""
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.err
        assert "Inputs: (10, 0), {}" in captured.err
        assert "ERROR" in captured.err

    def test_log_file_success(self) -> None:
        """Тестирует логирование успешного выполнения в файл."""
        test_file = "test_log.txt"

        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except PermissionError:
                pass

        result = multiply(4, 5)
        assert result == 20

        assert os.path.exists(test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "multiply ok" in content
            assert "INFO" in content

        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except PermissionError:
                pass

    def test_log_file_error(self) -> None:
        """Тестирует логирование ошибки в файл."""
        test_file = "test_log.txt"

        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except PermissionError:
                pass

        with pytest.raises(ValueError, match="Test error message"):
            failing_function(10)

        assert os.path.exists(test_file)

        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "failing_function error: ValueError" in content
            assert "Inputs: (10,), {}" in content
            assert "ERROR" in content

        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except PermissionError:
                pass

    def test_log_with_custom_filename(self) -> None:
        """Тестирует логирование в файл с пользовательским именем."""
        custom_file = "custom_log.txt"

        @log(filename=custom_file)
        def custom_func(x: int) -> int:
            return x * 2

        if os.path.exists(custom_file):
            try:
                os.remove(custom_file)
            except PermissionError:
                pass

        result = custom_func(10)
        assert result == 20

        assert os.path.exists(custom_file)

        with open(custom_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "custom_func ok" in content

        if os.path.exists(custom_file):
            try:
                os.remove(custom_file)
            except PermissionError:
                pass

    def test_log_with_kwargs(self, capsys) -> None:
        """Тестирует логирование с именованными аргументами."""

        @log()
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        result = greet(name="World", greeting="Hi")
        assert result == "Hi, World!"

        captured = capsys.readouterr()
        assert "greet ok" in captured.err

    def test_log_file_error_when_cannot_create_file(self, capsys) -> None:
        """Тестирует обработку ошибки при создании файла."""
        invalid_path = "/invalid_directory/log.txt"

        @log(filename=invalid_path)
        def test_func() -> str:
            return "test"

        import sys

        if sys.platform == "win32":
            pytest.skip("Skipping on Windows")

        result = test_func()
        assert result == "test"

        captured = capsys.readouterr()
        assert "Не удалось создать файл" in captured.err

    def test_log_preserves_function_metadata(self) -> None:
        """Тестирует, что декоратор сохраняет метаданные функции."""

        @log()
        def test_func(a: int, b: int) -> int:
            """Тестовая функция."""
            return a + b

        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "Тестовая функция."

    def test_log_with_temp_directory(self, temp_log_dir) -> None:
        """Тестирует логирование во временную директорию."""
        log_file = os.path.join(temp_log_dir, "temp_log.txt")

        @log(filename=log_file)
        def temp_func(x: int) -> int:
            return x * 3

        result = temp_func(5)
        assert result == 15

        assert os.path.exists(log_file)

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "temp_func ok" in content
