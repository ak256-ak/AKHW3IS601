class Calculation:
    def __init__(self, operation, a, b, result):
        self.operation = operation
        self.a = a
        self.b = b
        self.result = result

class Calculator:
    history = []

    def add(self, a, b):
        result = a + b
        Calculator.history.append(Calculation('add', a, b, result))
        return result

    def subtract(self, a, b):
        result = a - b
        Calculator.history.append(Calculation('subtract', a, b, result))
        return result

    def multiply(self, a, b):
        result = a * b
        Calculator.history.append(Calculation('multiply', a, b, result))
        return result

    def divide(self, a, b):
        if b == 0:
            return "Cannot divide by zero."
        result = a / b
        Calculator.history.append(Calculation('divide', a, b, result))
        return result

    @classmethod
    def show_history(cls):
        print("Calculation History:")
        for calc in cls.history:
            print(f"{calc.operation.capitalize()} of {calc.a} and {calc.b} is {calc.result}.")

calc = Calculator()

while True:
    try:
        a = float(input("Please enter a number: "))
        b = float(input("Please enter another number: "))
        operation = input("What would you like to do? (+, -, *, /) or type 'quit' to exit: ")

        if operation == '+':
            result = calc.add(a, b)
            print(f"The result of adding {a} and {b} is {result}.")

        elif operation == '-':
            result = calc.subtract(a, b)
            print(f"The result of subtracting {b} from {a} is {result}.")

        elif operation == '*':
            result = calc.multiply(a, b)
            print(f"The result of multiplying {a} and {b} is {result}.")

        elif operation == '/':
            result = calc.divide(a, b)
            print(f"The result of dividing {a} by {b} is {result}.")
        
        elif operation.lower() == 'quit':
            print("Goodbye!")
            break

        else:
            print("Invalid operation. Please choose: +, -, *, or /.")

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
