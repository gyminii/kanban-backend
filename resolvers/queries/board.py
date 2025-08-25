# resolvers/queries/board.py
import strawberry
from typing import List, Optional
from strawberry.types import Info

from models import BoardModel
from utils.serialize import to_board_type
from utils.auth import require_user
from gql.types import Board  # <-- import actual Strawberry type

@strawberry.type
class Query:
    @strawberry.field
    def boards(self, info: Info) -> List[Board]:  # <-- use Board, not "Board"
        user_id = require_user(info)
        docs = BoardModel.list_for_user(user_id)
        return [to_board_type(b) for b in docs]

    @strawberry.field
    def board(self, info: Info, board_id: strawberry.ID) -> Optional[Board]:
        user_id = require_user(info)
        b = BoardModel.by_id(str(board_id))
        if not b:
            return None
        if not (b["owner_id"] == user_id or user_id in b.get("members", [])):
            raise Exception("Forbidden")
        return to_board_type(b)
