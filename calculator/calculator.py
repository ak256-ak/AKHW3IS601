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
        command.result = result  
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
