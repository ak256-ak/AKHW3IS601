

from calculator.calculator import Calculator

def main():
    calc = Calculator()

    while True:
        try:
            a = input("Please enter a number: ")
            b = input("Please enter another number: ")
            operation = input("Please choose an operation (+, -, *, /), 'history' to view history, or 'quit' to exit: ")

            if operation == 'quit':
                print("Thank you for using the calculator!")
                break
            elif operation == 'history':
                print(calc.show_history())
            else:
                result = calc.calculate_from_input(a, b, operation)
                print(f"Result: {result}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
