

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



