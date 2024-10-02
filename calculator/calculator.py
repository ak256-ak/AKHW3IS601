class Calculation:
    def __init__(self, operation, a, b, result):
        self.operation = operation
        self.a = a
        self.b = b
        self.result = result

class Calculator:
    history = []

    def add(self, a, b):
        """Adding numbers and saving it to the history!"""
        result = a + b
        Calculator.history.append(Calculation('add', a, b, result))
        return result

    def subtract(self, a, b):
        """Subtracting and storing the result for future reference!"""
        result = a - b
        Calculator.history.append(Calculation('subtract', a, b, result))
        return result

    def multiply(self, a, b):
        """Multiplying these two and putting the result in the history!"""
        result = a * b
        Calculator.history.append(Calculation('multiply', a, b, result))
        return result

    def divide(self, a, b):
        """Dividing these numbers, unless you're trying to divide by zero!"""
        if b == 0:
            return "Cannot divide by zero."
        result = a / b
        if result.is_integer():
            result = int(result)  # If it's a whole number, return it as an integer
        Calculator.history.append(Calculation('divide', a, b, result))
        return result

    @classmethod
    def show_history(cls):
        """Here’s everything you've calculated so far!"""
        if not cls.history:
            return "No history available."
        else:
            history_str = "Calculation History:\n"
            for calc in cls.history:
                history_str += f"{calc.operation.capitalize()} of {calc.a} and {calc.b} is {calc.result}\n"
            return history_str

    @classmethod
    def clear_history(cls):
        """Yeah! History has been cleared!"""
        cls.history.clear()
        return "History cleared."

    def calculate_from_input(a, b, operation):
        """Let's figure out what operation to perform and get the result."""
        calc = Calculator()
        try:
            a = float(a)
            b = float(b)
        except ValueError:
            return f"Oops, {a} or {b} isn't a valid number."

        if operation == 'add':
            return calc.add(a, b)
        elif operation == 'subtract':
            return calc.subtract(a, b)
        elif operation == 'multiply':
            return calc.multiply(a, b)
        elif operation == 'divide':
            return calc.divide(a, b)
        else:
            return f"Unknown operation: {operation}"
