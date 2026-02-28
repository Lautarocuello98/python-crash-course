import pytest
from employee import Employee

@pytest.fixture
def employee():
    return Employee("Lautaro", "Cuello", 50000)

def test_give_default_raise(employee):
    employee.give_raise()
    assert employee.annual_salary == 55000

def test_give_custom_raise(employee):
    employee.give_raise(12000)
    assert employee.annual_salary == 62000