# resolvers/mutations/column.py
import strawberry
from strawberry.types import Info

from models import BoardModel, ColumnModel
from utils.serialize import to_column_type
from utils.dnd import reorder_columns_within_board, clamp
from gql.types import Column 


@strawberry.type
class ColumnMutation:
    @strawberry.mutation
    def add_column(self, info: Info, board_id: strawberry.ID, title: str) -> Column:
        b = BoardModel.by_id(str(board_id))
        if not b:
            raise Exception("Board not found")

        order = BoardModel.column_count(b["_id"])
        col = ColumnModel.create(b["_id"], title, order)
        return to_column_type(col, include_cards=True)

    @strawberry.mutation
    def move_column(self, info: Info, column_id: strawberry.ID, new_order: int) -> Column:
        col = ColumnModel.by_id(str(column_id))
        if not col:
            raise Exception("Column not found")

        board_oid = col["board_id"]  # already an ObjectId
        count = BoardModel.column_count(board_oid)
        new_order = clamp(new_order, 0, max(0, count - 1))
        old_order = int(col.get("order", 0))
        if new_order != old_order:
            reorder_columns_within_board(board_oid, old_order, new_order)
            ColumnModel.update_order(col["_id"], new_order)

        return to_column_type(ColumnModel.by_id(str(col["_id"])), include_cards=True)
