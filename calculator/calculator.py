'''
import os
import importlib
import multiprocessing
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def worker(command, result_queue):
    result_queue.put(command.execute())

class Command:
    def execute(self):
        pass

class Calculator:
    history = []

    def execute_command(self, command: Command):
        result_queue = multiprocessing.Queue()

        process = multiprocessing.Process(target=worker, args=(command, result_queue))
        process.start()
        process.join()

        result = result_queue.get()
        command.result = result  # Store the result in the command
        Calculator.history.append(command)
        return result

    @classmethod
    def show_history(cls):
        if not cls.history:
            return "No history available."
        else:
            history_str = "Calculation History:\n"
            for calc in cls.history:
                history_str += f"{calc.__class__.__name__} of {calc.a} and {calc.b} is {calc.result}\n"
            return history_str

    @classmethod
    def clear_history(cls):
        cls.history.clear()
        return "History cleared."

def load_plugins():
    plugin_directory = './calculator/plugins'
    plugins = {}
    for filename in os.listdir(plugin_directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'calculator.plugins.{module_name}')
            command_name = module_name.capitalize() + "Command"
            plugins[module_name] = getattr(module, command_name)
    return plugins

def show_menu(plugins):
    print("Available commands:")
    for command_name in plugins.keys():
        print(f" - {command_name}")
    print(" - menu")
    print(" - exit")

def repl():
    calc = Calculator()
    plugins = load_plugins()
    show_menu(plugins)
    while True:
        operation = input("Enter command or 'menu' to see available commands, or 'exit' to quit: ").lower()
        if operation == 'exit':
            break
        elif operation == 'menu':
            show_menu(plugins)
        elif operation in plugins:
            try:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
            except ValueError:
                print("Invalid number. Try again.")
                continue

            command = plugins[operation](a, b)
            result = calc.execute_command(command)
            print(f"Result: {result}")
        else:
            print("Unknown  command. Try again.")

if __name__ == "__main__":
    repl()
'''

'''
import os
import importlib
import multiprocessing
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def worker(command, result_queue):
    try:
        result_queue.put(command.execute())  # Line 13: Now covered with exception handling
    except Exception as e:
        result_queue.put(f"Error: {e}")


class Command:
    def execute(self):
        pass


class Calculator:
    history = []

    def execute_command(self, command: Command):
        result_queue = multiprocessing.Queue()

        process = multiprocessing.Process(target=worker, args=(command, result_queue))
        process.start()
        process.join()

        result = result_queue.get()
        command.result = result  # Store the result in the command
        Calculator.history.append(command)
        return result

    @classmethod
    def show_history(cls):
        if not cls.history:
            return "No history available."
        else:
            history_str = "Calculation History:\n"
            for calc in cls.history:
                history_str += f"{calc.__class__.__name__} of {calc.a} and {calc.b} is {calc.result}\n"
            return history_str

    @classmethod
    def clear_history(cls):
        cls.history.clear()
        return "History cleared."


def load_plugins():
    plugin_directory = './calculator/plugins'
    plugins = {}
    for filename in os.listdir(plugin_directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'calculator.plugins.{module_name}')
            command_name = module_name.capitalize() + "Command"
            plugins[module_name] = getattr(module, command_name)
    return plugins


def show_menu(plugins):
    print("Available commands:")
    for command_name in plugins.keys():
        print(f" - {command_name}")
    print(" - menu")
    print(" - exit")


def repl():
    calc = Calculator()
    plugins = load_plugins()
    show_menu(plugins)
    while True:
        operation = input("Enter command or 'menu' to see available commands, or 'exit' to quit: ").lower()
        if operation == 'exit':
            break
        elif operation == 'menu':
            show_menu(plugins)
        elif operation in plugins:
            try:
                a = float(input("Enter first number: "))
                b_input = input("Enter second number: ")
                if b_input.strip() == "":  # Handles missing input for second number (Lines 77-79)
                    print("Second number is missing. Try again.")
                    continue
                b = float(b_input)
            except ValueError:
                print("Invalid number. Try again.")
                continue

            command = plugins[operation](a, b)
            result = calc.execute_command(command)
            print(f"Result: {result}")
        else:
            print("Unknown command. Try again.")  # Line 88: Handles unknown commands


# Test cases added directly to calculator.py for coverage
if __name__ == "__main__":
    # Test worker function coverage (Line 13)
    class MockCommand(Command):
        def __init__(self, result):
            self.result = result

        def execute(self):
            return self.result

    def test_worker_function():
        calc = Calculator()
        command = MockCommand(42)
        result = calc.execute_command(command)
        assert result == 42
        print("Worker function test passed!")

    # Test invalid second input handling (Lines 77-79)
    def test_invalid_second_input():
        with patch('builtins.input', side_effect=['add', '10', '', 'exit']):
            with patch('builtins.print') as mock_print:
                repl()
                mock_print.assert_any_call("Second number is missing. Try again.")

    # Test unknown command handling (Line 88)
    def test_unknown_command():
        with patch('builtins.input', side_effect=['unknown', 'exit']):
            with patch('builtins.print') as mock_print:
                repl()
                mock_print.assert_any_call("Unknown command. Try again.")

    # Run the test cases for coverage
    test_worker_function()
    test_invalid_second_input()
    test_unknown_command()

    # Start REPL if running as main
    repl()
'''

import os
import importlib
import multiprocessing
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def worker(command, result_queue):
    try:
        result_queue.put(command.execute())
    except Exception as e:
        result_queue.put(f"Error: {e}")

class Command:
    def execute(self):
        pass

class Calculator:
    history = []

    def execute_command(self, command: Command):
        result_queue = multiprocessing.Queue()

        try:
            process = multiprocessing.Process(target=worker, args=(command, result_queue))
            process.start()
            process.join()

            result = result_queue.get()
            command.result = result
            Calculator.history.append(command)
            return result
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    def show_history(cls):
        if not cls.history:
            return "No history available."
        history_str = "Calculation History:\n"
        for calc in cls.history:
            history_str += f"{calc.__class__.__name__} of {calc.a} and {calc.b} is {calc.result}\n"
        return history_str

    @classmethod
    def clear_history(cls):
        cls.history.clear()
        return "History cleared."

def load_plugins():
    plugin_directory = './calculator/plugins'
    plugins = {}
    for filename in os.listdir(plugin_directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f'calculator.plugins.{module_name}')
                command_name = module_name.capitalize() + "Command"
                plugins[module_name] = getattr(module, command_name)
            except ImportError as e:
                print(f"Error loading plugin {module_name}: {e}")
    return plugins

def get_input(prompt):
    return input(prompt)

def repl():
    calc = Calculator()
    plugins = load_plugins()
    print("Available commands:")
    for command in plugins:
        print(f"- {command}")
    while True:
        operation = get_input("Enter command or 'exit' to quit: ").lower()
        if operation == 'exit':
            break
        elif operation in plugins:
            try:
                a = float(get_input("Enter first number: "))
                b_input = get_input("Enter second number: ")
                if not b_input:
                    print("Second number is missing. Try again.")
                    continue
                b = float(b_input)
                command = plugins[operation](a, b)
                result = calc.execute_command(command)
                print(f"Result: {result}")
            except ValueError:
                print("Invalid number. Try again.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Unknown command. Try again.")



