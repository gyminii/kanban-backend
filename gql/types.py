import strawberry
from typing import List, Optional
from datetime import datetime

# Tasks for each column (sprint)
@strawberry.type
class Card:
    id: strawberry.ID
    column_id: strawberry.ID
    title: str
    description: Optional[str]
    order: int
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]   
    completed: bool    
    
# Sprint each week
@strawberry.type
class Column:
    id: strawberry.ID
    board_id: strawberry.ID
    title: str
    order: int
    cards: List[Card]

# Project or entire board
@strawberry.type
class Board:
    id: strawberry.ID
    title: str
    owner_id: str
    members: List[str]
    created_at: datetime
    updated_at: datetime
    columns: List[Column]
