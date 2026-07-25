from pydantic import BaseModel
from typing import Optional, Literal
class ExpenseSplit(BaseModel):
    username: str
    amount: Optional[float] = None
    percentage: Optional[float] = None
    
class ExpenseCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    split_type: Literal["equal", "exact", "percentage"]
    split_with: list[str] | list[ExpenseSplit]