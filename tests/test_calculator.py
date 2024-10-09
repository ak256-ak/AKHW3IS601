import sys
import os
from unittest.mock import patch
import pytest
from calculator.calculator import Calculator, repl, load_plugins
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.multiply import MultiplyCommand

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def test_repl_add_command():
    with patch('builtins.input', side_effect=['add', '5', '3', 'exit']):
        repl()

def test_repl_exit():
    with patch('builtins.input', side_effect=['exit']):
        repl()

def test_repl_menu():
    with patch('builtins.input', side_effect=['menu', 'exit']):
        repl()

def test_repl_invalid_command():
    with patch('builtins.input', side_effect=['invalid_command', 'exit']):
        repl()

def test_repl_no_input():
    with patch('builtins.input', side_effect=['', 'exit']):
        repl()

def test_load_plugins_success():
    plugins = load_plugins()
    assert 'add' in plugins
    assert 'subtract' in plugins
    assert 'multiply' in plugins
    assert 'divide' in plugins

def test_load_plugins_invalid_module():
    with patch('os.listdir', return_value=['invalid_plugin.py']):
        with pytest.raises(ImportError):
            load_plugins()

def test_load_plugins_no_plugins():
    with patch('os.listdir', return_value=[]):
        plugins = load_plugins()
        assert plugins == {}

def test_execute_command_multiprocessing():
    calc = Calculator()
    calc.clear_history()
    add_command = AddCommand(5, 3)
    result = calc.execute_command(add_command)
    assert result == 8
    assert len(calc.history) == 1

class InvalidCommand:
    def execute(self):
        pass

def test_invalid_command_execution():
    calc = Calculator()
    invalid_command = InvalidCommand()
    result = calc.execute_command(invalid_command)
    assert result is None
