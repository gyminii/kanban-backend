import strawberry
from typing import Optional, List
from strawberry.types import Info
from datetime import datetime

from models import BoardModel, ColumnModel, CardModel
from utils.serialize import to_card_type
from utils.dnd import clamp, remove_gap_in_column, make_space_in_column, reorder_within_column
from gql.types import Card


@strawberry.type
class CardMutation:
    @strawberry.mutation
    def add_card(
        self,
        info: Info,
        column_id: strawberry.ID,
        title: str,
        description: Optional[str] = None,
        assigned_to: Optional[str] = None,
        due_date: Optional[datetime] = None,
        completed: Optional[bool] = False,
        tags: Optional[List[str]] = None, 
    ) -> Card:
        col = ColumnModel.by_id(str(column_id))
        if not col:
            raise Exception("Column not found")

        order = CardModel.count_in_column(col["_id"])
        card = CardModel.create(
            col["_id"], title, description, order, assigned_to, due_date, bool(completed), tags or [], 
        )
        return to_card_type(card)

    @strawberry.mutation
    def update_card(
        self,
        info: Info,
        card_id: strawberry.ID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        assigned_to: Optional[str] = None,
        due_date: Optional[datetime] = None,
        completed: Optional[bool] = None,
        archived: Optional[bool] = None, 
        tags: Optional[List[str]] = None,
    ) -> Card:
        c = CardModel.by_id(str(card_id))
        if not c:
            raise Exception("Card not found")

        patch = {}
        if title is not None:
            patch["title"] = title
        if description is not None:
            patch["description"] = description
        if assigned_to is not None:
            patch["assigned_to"] = assigned_to
        if due_date is not None:
            patch["due_date"] = due_date
        if completed is not None:
            patch["completed"] = bool(completed)
        if archived is not None: 
            patch["archived"] = bool(archived) 
        if tags is not None:     
            patch["tags"] = list(tags)
        if patch:
            CardModel.update(c["_id"], patch)

        return to_card_type(CardModel.by_id(str(c["_id"])))

    @strawberry.mutation
    def move_card(
        self,
        info: Info,
        card_id: strawberry.ID,
        new_column_id: strawberry.ID,
        new_order: int,
    ) -> Card:
        c = CardModel.by_id(str(card_id))
        if not c:
            raise Exception("Card not found")

        from_col = ColumnModel.by_id(str(c["column_id"]))
        if not from_col:
            raise Exception("Source column not found")

        to_col = ColumnModel.by_id(str(new_column_id))
        if not to_col:
            raise Exception("Target column not found")
        if str(to_col["board_id"]) != str(from_col["board_id"]):
            raise Exception("Cannot move card across boards")

        if to_col["_id"] == from_col["_id"]:
            count = CardModel.count_in_column(from_col["_id"])
            new_order = clamp(new_order, 0, max(0, count - 1))
            old_order = int(c.get("order", 0))
            reorder_within_column(from_col["_id"], old_order, new_order)
            CardModel.update(c["_id"], {"order": new_order})
        else:
            old_order = int(c.get("order", 0))
            remove_gap_in_column(from_col["_id"], old_order)
            count = CardModel.count_in_column(to_col["_id"])
            new_order = clamp(new_order, 0, count)
            make_space_in_column(to_col["_id"], new_order)
            CardModel.update(c["_id"], {"column_id": to_col["_id"], "order": new_order})

        return to_card_type(CardModel.by_id(str(c["_id"])))

    # --- NEW: delete a card and compact orders in its column ---
    @strawberry.mutation
    def delete_card(self, info: Info, card_id: strawberry.ID) -> bool:
        c = CardModel.by_id(str(card_id))
        if not c:
            return False
        col_oid = c["column_id"]
        old_order = int(c.get("order", 0))
        CardModel.delete(c["_id"])
        # Close the order gap in the column for remaining cards
        remove_gap_in_column(col_oid, old_order)
        return True
