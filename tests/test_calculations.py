# This is unnecessary file (I am use this for introduce myself testing using Pytest in general)
import pytest

from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFundsException


# Fixtures
@pytest.fixture
def zero_bank_account():
    """BankAccount instance starting_balance=0"""
    print("creating empty bank account")
    return BankAccount()


@pytest.fixture
def bank_account():
    """BankAccount instance starting_balance=50"""
    return BankAccount(50)


# Parameterized test
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 3, 6),
    (5, 5, 10),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(20, 5) == 4


# Using Fixture insead repeated initilizing new instance of BankAccount
def test_bank_set_initial_amount(bank_account: BankAccount):
    # bank_account = BankAccount(90)
    # assert bank_account.balance == 90
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    # assert bank_account.balance == 0
    print("testing my bank account")
    assert zero_bank_account.balance == 0


def test_bank_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20


def test_bank_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 100


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


# Test Using Parameterize and Fixture
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (60, 30, 30),
    (200, 100, 100),
    (1200, 200, 1000),
    #(100, 500, -400)  # raise Exception (InsufficientFundsException to withdrew)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


# For case when raising any expected Exception
def test_bank_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFundsException):
        bank_account.withdraw(500)
