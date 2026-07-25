import pytest
from schemas.expense import ExpenseCreate, ExpenseSplit
from services.expense_service import split_expense

def test_split_expense_equal_strings():
    expense = ExpenseCreate(
        amount=100.0,
        description="Dinner",
        split_type="equal",
        split_with=["alice", "bob", "charlie"]
    )
    result = split_expense(expense)
    assert result == {"alice": 33.34, "bob": 33.33, "charlie": 33.33}
    assert sum(result.values()) == 100.0

def test_split_expense_equal_objects():
    expense = ExpenseCreate(
        amount=60.00,
        description="Lunch",
        split_type="equal",
        split_with=[
            ExpenseSplit(username="alice"),
            ExpenseSplit(username="bob"),
            ExpenseSplit(username="charlie")
        ]
    )
    result = split_expense(expense)
    assert result == {"alice": 20.0, "bob": 20.0, "charlie": 20.0}
    assert sum(result.values()) == 60.0

def test_split_expense_exact_valid():
    expense = ExpenseCreate(
        amount=100.0,
        description="Cab",
        split_type="exact",
        split_with=[
            ExpenseSplit(username="alice", amount=50.0),
            ExpenseSplit(username="bob", amount=30.0),
            ExpenseSplit(username="charlie", amount=20.0)
        ]
    )
    result = split_expense(expense)
    assert result == {"alice": 50.0, "bob": 30.0, "charlie": 20.0}

def test_split_expense_exact_invalid():
    expense = ExpenseCreate(
        amount=100.0,
        description="Cab",
        split_type="exact",
        split_with=[
            ExpenseSplit(username="alice", amount=50.0),
            ExpenseSplit(username="bob", amount=30.0),
            ExpenseSplit(username="charlie", amount=10.0) # Sum is 90
        ]
    )
    with pytest.raises(ValueError, match="The sum of split amounts must equal the total expense amount."):
        split_expense(expense)

def test_split_expense_percentage_valid():
    expense = ExpenseCreate(
        amount=200.0,
        description="Hotel",
        split_type="percentage",
        split_with=[
            ExpenseSplit(username="alice", percentage=50.0),
            ExpenseSplit(username="bob", percentage=30.0),
            ExpenseSplit(username="charlie", percentage=20.0)
        ]
    )
    result = split_expense(expense)
    assert result == {"alice": 100.0, "bob": 60.0, "charlie": 40.0}

def test_split_expense_percentage_invalid():
    expense = ExpenseCreate(
        amount=200.0,
        description="Hotel",
        split_type="percentage",
        split_with=[
            ExpenseSplit(username="alice", percentage=50.0),
            ExpenseSplit(username="bob", percentage=30.0),
            ExpenseSplit(username="charlie", percentage=10.0) # Sum is 90%
        ]
    )
    with pytest.raises(ValueError, match="The sum of percentages must equal 100."):
        split_expense(expense)
