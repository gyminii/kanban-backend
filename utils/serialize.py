# utils/serialize.py
from typing import Dict, Any
from models import ColumnModel, CardModel
from gql.types import Board, Column, Card  # real Strawberry types

def to_card_type(doc: Dict[str, Any]) -> Card:
    return Card(
        id=str(doc["_id"]),
        column_id=str(doc["column_id"]),
        title=doc.get("title", ""),
        description=doc.get("description"),
        order=int(doc.get("order", 0)),
        assigned_to=doc.get("assigned_to"),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
        due_date=doc.get("due_date"),       
        completed=bool(doc.get("completed", False)),
    )

def to_column_type(doc: Dict[str, Any], include_cards: bool = True) -> Column:
    cards = []
    if include_cards:
        cards = [to_card_type(c) for c in CardModel.list_for_column(doc["_id"])]
    return Column(
        id=str(doc["_id"]),
        board_id=str(doc["board_id"]),
        title=doc.get("title", ""),
        order=int(doc.get("order", 0)),
        cards=cards,
    )

def to_board_type(doc: Dict[str, Any]) -> Board:
    cols = [to_column_type(c, include_cards=True) for c in ColumnModel.list_for_board(doc["_id"])]
    return Board(
        id=str(doc["_id"]),
        title=doc.get("title", ""),
        owner_id=doc.get("owner_id"),
        members=doc.get("members", []),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
        columns=cols,
    )
