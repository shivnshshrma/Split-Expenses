from database.connection import SessionLocal
from database.models import Expense

async def create_expense(expense):
    serialized_split_with = []
    for item in expense.split_with:
        if isinstance(item, str):
            serialized_split_with.append(item)
        else:
            if hasattr(item, "model_dump"):
                serialized_split_with.append(item.model_dump())
            else:
                serialized_split_with.append(item.dict())

    with SessionLocal() as db:
        db_expense = Expense(
            amount=expense.amount,
            description=expense.description,
            split_type=expense.split_type,
            split_with=serialized_split_with
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return {
            "id": db_expense.id,
            "amount": db_expense.amount,
            "description": db_expense.description,
            "split_type": db_expense.split_type,
            "split_with": db_expense.split_with
        }
    
async def get_group_expenses(group_id: str):
    with SessionLocal() as db:
        expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
        return [
            {
                "id": e.id,
                "group_id": e.group_id,
                "amount": e.amount,
                "description": e.description,
                "split_type": e.split_type,
                "split_with": e.split_with
            }
            for e in expenses
        ]


def split_expense(expense):
    if expense.split_type == "equal":
        # if the split is equal 
        split_people = len(expense.split_with)
        # take the total number of people in the expense

        share = round(expense.amount / split_people, 2)
        # each person pays equal share
        
        # expense.split_with can be a list of strings or list of ExpenseSplit. Let's extract usernames.
        usernames = [
            item if isinstance(item, str) else item.username 
            for item in expense.split_with
        ]
        
        splits = {username: share for username in usernames}

        #Handling rounding reminders
        difference = round(expense.amount - sum(splits.values()), 2)
        if difference != 0:
            #Add reminder to the first person
            splits[usernames[0]] = round(splits[usernames[0]] + difference, 2)
    
    elif expense.split_type == "exact":
        # Expense are entered manually by the user
        try:
            # sum of total split amount should be equal to the total expense amount
            total_split_amount = sum(item.amount for item in expense.split_with)
            if abs(total_split_amount - expense.amount) > 0.01:
                raise ValueError("The sum of split amounts must equal the total expense amount.")
        except TypeError:
            raise ValueError("Invalid split_with format for exact split.")
        # assign amount to other people
        splits = {item.username: item.amount for item in expense.split_with}
    elif expense.split_type == "percentage":
        try:
            # total percentage should be 100
            total_percentage = sum(item.percentage for item in expense.split_with)
            if abs(total_percentage - 100) > 0.01:
                raise ValueError("The sum of percentages must equal 100.")
        except TypeError:
            raise ValueError("Invalid split_with format for percentage split.")
        #assign amount according to the percentage
        splits = {item.username: item.percentage * expense.amount / 100 for item in expense.split_with}
    else:
        raise ValueError("Invalid split_type. Supported types: 'equal', 'exact', 'percentage'.")

    return splits
