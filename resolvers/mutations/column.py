import strawberry
from typing import Optional
from datetime import datetime
from strawberry.types import Info

from models import BoardModel, ColumnModel, CardModel
from utils.serialize import to_column_type
from utils.dnd import reorder_columns_within_board, clamp
from gql.types import Column  # real type

@strawberry.type
class ColumnMutation:
    @strawberry.mutation
    def add_column(
        self,
        info: Info,
        board_id: strawberry.ID,
        title: str,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
    ) -> Column:
        b = BoardModel.by_id(str(board_id))
        if not b:
            raise Exception("Board not found")

        order = BoardModel.column_count(b["_id"])
        col = ColumnModel.create(
            b["_id"],
            title=title,
            order=order,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )
        return to_column_type(col, include_cards=True)

    @strawberry.mutation
    def move_column(self, info: Info, column_id: strawberry.ID, new_order: int) -> Column:
        col = ColumnModel.by_id(str(column_id))
        if not col:
            raise Exception("Column not found")
        b = BoardModel.by_id(str(col["board_id"]))
        if not b:
            raise Exception("Board not found")

        board_oid = b["_id"]
        count = BoardModel.column_count(board_oid)
        new_order = clamp(new_order, 0, max(0, count - 1))
        old_order = int(col.get("order", 0))
        if new_order != old_order:
            reorder_columns_within_board(board_oid, old_order, new_order)
            ColumnModel.update_order(col["_id"], new_order)

        return to_column_type(ColumnModel.by_id(str(col["_id"])), include_cards=True)

    # --- NEW: update non-order fields of a column ---
    @strawberry.mutation
    def update_column(
        self,
        info: Info,
        column_id: strawberry.ID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
    ) -> Column:
        col = ColumnModel.by_id(str(column_id))
        if not col:
            raise Exception("Column not found")

        patch = {}
        if title is not None:
            patch["title"] = title
        if description is not None:
            patch["description"] = description
        if start_date is not None:
            patch["start_date"] = start_date
        if end_date is not None:
            patch["end_date"] = end_date
        if status is not None:
            patch["status"] = status

        if patch:
            ColumnModel.update(col["_id"], patch)

        return to_column_type(ColumnModel.by_id(str(col["_id"])), include_cards=True)

    # --- NEW: delete a column + cascade delete its cards and compact orders ---
    @strawberry.mutation
    def delete_column(self, info: Info, column_id: strawberry.ID) -> bool:
        col = ColumnModel.by_id(str(column_id))
        if not col:
            return False

        board_oid = col["board_id"]
        removed_order = int(col.get("order", 0))

        # Delete cards in the column
        CardModel.delete_in_column(col["_id"])
        # Delete the column
        ColumnModel.delete(col["_id"])
        # Compact remaining column orders in the board
        ColumnModel.compact_orders(board_oid, removed_order)

        return True
