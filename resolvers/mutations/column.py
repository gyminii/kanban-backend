# resolvers/mutations/column.py
import strawberry
from strawberry.types import Info

from models import BoardModel, ColumnModel
from utils.serialize import to_column_type
from utils.auth import require_user
from utils.dnd import reorder_columns_within_board, clamp
from gql.types import Column  # <-- import

@strawberry.type
class ColumnMutation:
    @strawberry.mutation
    def add_column(self, info: Info, board_id: strawberry.ID, title: str) -> Column:
        user_id = require_user(info)
        b = BoardModel.by_id(str(board_id))
        if not b:
            raise Exception("Board not found")
        if not (b["owner_id"] == user_id or user_id in b.get("members", [])):
            raise Exception("Forbidden")

        order = BoardModel.column_count(b["_id"])
        col = ColumnModel.create(b["_id"], title, order)
        return to_column_type(col, include_cards=True)

    @strawberry.mutation
    def move_column(self, info: Info, column_id: strawberry.ID, new_order: int) -> Column:
        user_id = require_user(info)
        col = ColumnModel.by_id(str(column_id))
        if not col:
            raise Exception("Column not found")
        b = BoardModel.by_id(str(col["board_id"]))
        if not (b["owner_id"] == user_id or user_id in b.get("members", [])):
            raise Exception("Forbidden")

        board_oid = b["_id"]
        count = BoardModel.column_count(board_oid)
        new_order = clamp(new_order, 0, max(0, count - 1))
        old_order = int(col.get("order", 0))
        if new_order != old_order:
            reorder_columns_within_board(board_oid, old_order, new_order)
            ColumnModel.update_order(col["_id"], new_order)

        return to_column_type(ColumnModel.by_id(str(col["_id"])), include_cards=True)
