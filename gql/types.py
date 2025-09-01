# gql/types.py
import strawberry
from typing import List, Optional
from datetime import datetime

@strawberry.type
class Card:
    id: strawberry.ID
    board_id: strawberry.ID
    column_id: strawberry.ID
    board_id: strawberry.ID  
    title: str
    description: Optional[str]
    order: int
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    archived: Optional[bool] = None
    tags: List[str] 

@strawberry.type
class Column:
    id: strawberry.ID
    board_id: strawberry.ID
    title: str
    order: int
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[str]
    created_at: datetime
    updated_at: datetime
    cards: List[Card]

@strawberry.type
class Board:
    id: strawberry.ID
    title: str
    owner_id: str
    members: List[str]
    description: Optional[str]
    color: Optional[str]
    is_favorite: bool
    is_archived: bool
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    columns: List[Column]
