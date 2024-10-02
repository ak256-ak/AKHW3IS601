import pytest
from calculator.calculator import Calculator

calc = Calculator()

@pytest.mark.parametrize("a, b, operation, expected_result", [
    (5, 3, 'add', "The result of 5 add 3 is 8"),
    (10, 2, 'subtract', "The result of 10 subtract 2 is 8"),
    (4, 5, 'multiply', "The result of 4 multiply 5 is 20"),
    (20, 4, 'divide', "The result of 20 divide 4 is 5"),
    (1, 0, 'divide', "Cannot divide by zero."),
    ("a", 3, 'add', "Invalid number input: a or 3 is not a valid number.")
])
def test_calculate_and_print(a, b, operation, expected_result, capsys):
    if isinstance(a, str) or isinstance(b, str):
        print(f"Invalid number input: {a} or {b} is not a valid number.")
    else:
        result = getattr(calc, operation)(a, b)
        if result == "Cannot divide by zero.":
            print(result)  # Directly print the error message
        else:
            print(f"The result of {a} {operation} {b} is {result}")
    
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result

def test_generate_fake_data(generate_fake_data, capsys):
    for a, b, operation, expected_result in generate_fake_data:
        result = getattr(calc, operation)(a, b)
        if result == "Cannot divide by zero.":
            print(result)  # Directly print the error message
        else:
            print(f"The result of {a} {operation} {b} is {result}")
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result
