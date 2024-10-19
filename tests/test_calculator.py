
import sys
import os
from unittest.mock import patch
import pytest
from calculator.calculator import Calculator, repl, load_plugins, Command
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.multiply import MultiplyCommand

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MockCommand(Command):
    def __init__(self, a=0, b=0, result=42):
        self.a = a
        self.b = b
        self.result = result

    def execute(self):
        return self.result

class ErrorCommand(Command):
    def execute(self):
        raise ValueError("Test error")

def test_add_command():
    add_command = AddCommand(5, 3)
    result = add_command.execute()
    assert result == 8

def test_subtract_command():
    subtract_command = SubtractCommand(10, 5)
    result = subtract_command.execute()
    assert result == 5

def test_multiply_command():
    multiply_command = MultiplyCommand(6, 2)
    result = multiply_command.execute()
    assert result == 12

def test_divide_command():
    divide_command = DivideCommand(20, 4)
    result = divide_command.execute()
    assert result == 5

def test_divide_by_zero():
    divide_command = DivideCommand(5, 0)
    result = divide_command.execute()
    assert result == "Cannot divide by zero."

def test_calculator_execution():
    calc = Calculator()
    add_command = AddCommand(5, 3)
    result = calc.execute_command(add_command)
    assert result == 8
    assert len(calc.history) == 1

def test_clear_history():
    calc = Calculator()
    add_command = AddCommand(5, 3)
    calc.execute_command(add_command)
    calc.clear_history()
    assert len(calc.history) == 0

def test_show_history_with_items():
    calc = Calculator()
    add_command = AddCommand(5, 3)
    subtract_command = SubtractCommand(10, 5)
    calc.execute_command(add_command)
    calc.execute_command(subtract_command)
    history = calc.show_history()
    assert "AddCommand of 5 and 3 is 8" in history
    assert "SubtractCommand of 10 and 5 is 5" in history

def test_clear_history_after_operations():
    calc = Calculator()
    add_command = AddCommand(5, 3)
    subtract_command = SubtractCommand(10, 5)
    calc.execute_command(add_command)
    calc.execute_command(subtract_command)
    calc.clear_history()
    assert calc.show_history() == "No history available."

def test_repl_invalid_first_number():
    with patch('calculator.calculator.get_input', side_effect=['add', 'abc', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Invalid number. Try again.")

def test_repl_missing_second_number():
    with patch('calculator.calculator.get_input', side_effect=['add', '5', '', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Second number is missing. Try again.")

def test_repl_unknown_command():
    with patch('calculator.calculator.get_input', side_effect=['unknown', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Unknown command. Try again.")

def test_repl_error_handling():
    with patch('calculator.calculator.get_input', side_effect=['divide', '10', '0', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Result: Cannot divide by zero.")

def test_worker_function():
    calc = Calculator()
    command = MockCommand()
    result = calc.execute_command(command)
    assert result == 42

def test_worker_function_error_handling():
    calc = Calculator()
    command = ErrorCommand()
    result = calc.execute_command(command)
    assert "Error" in str(result)

def test_execute_command_unexpected_error():
    calc = Calculator()
    with patch('multiprocessing.Process.start', side_effect=Exception("Unexpected error")):
        result = calc.execute_command(MockCommand())
        assert "Error: Unexpected error" in result

def test_execute_command_process_failure():
    calc = Calculator()
    with patch('multiprocessing.Process.start', side_effect=Exception("Process failure")):
        result = calc.execute_command(MockCommand())
        assert "Error: Process failure" in result

def test_load_plugins_import_error():
    with patch('os.listdir', return_value=['invalid_plugin.py']):
        with patch('importlib.import_module', side_effect=ImportError("Import error")):
            plugins = load_plugins()
            assert 'invalid_plugin' not in plugins

def test_repl_missing_first_number():
    with patch('calculator.calculator.get_input', side_effect=['add', '', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Invalid number. Try again.")

def test_repl_process_failure():
    with patch('calculator.calculator.get_input', side_effect=['add', '5', '2', 'exit']):
        with patch('calculator.calculator.Calculator.execute_command', side_effect=Exception("Process failure")):
            with patch('builtins.print') as mock_print:
                repl()
                mock_print.assert_any_call("Error: Process failure")

def test_repl_unexpected_error():
    with patch('calculator.calculator.get_input', side_effect=['add', '5', '2', 'exit']):
        with patch('calculator.calculator.Calculator.execute_command', side_effect=Exception("Unexpected error")):
            with patch('builtins.print') as mock_print:
                repl()
                mock_print.assert_any_call("Error: Unexpected error")
