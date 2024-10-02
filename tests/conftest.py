import pytest
from faker import Faker
from calculator.calculator import Calculator  # Adjusted path based on your structure

fake = Faker()

def pytest_addoption(parser):
    parser.addoption("--num_records", action="store", default=10, type=int, help="Number of records to generate")

@pytest.fixture
def generate_fake_data(request):
    num_records = request.config.getoption("--num_records")
    test_data = []
    calc = Calculator()  # Instantiate your Calculator class
    for _ in range(num_records):
        a = fake.random_int(min=0, max=100)
        b = fake.random_int(min=0, max=100)
        operation = fake.random_element(elements=('add', 'subtract', 'multiply', 'divide'))
        
        if operation == 'divide' and b == 0:
            expected_result = "Cannot divide by zero."
        else:
            result = getattr(calc, operation)(a, b)  # Dynamically call the correct method
            expected_result = f"The result of {a} {operation} {b} is {result}"
        
        test_data.append((a, b, operation, expected_result))
    return test_data
