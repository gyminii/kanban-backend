# resolvers/queries/board.py
import strawberry
from typing import List, Optional
from strawberry.types import Info

from models import BoardModel
from utils.serialize import to_board_type
from gql.types import Board  

@strawberry.type
class Query:
    @strawberry.field
    def boards(self, info: Info, user_id: str) -> List[Board]:
        docs = BoardModel.list_for_user(user_id)
        return [to_board_type(b) for b in docs]

    @strawberry.field
    def board(self, info: Info, board_id: strawberry.ID) -> Optional[Board]:
        b = BoardModel.by_id(str(board_id))
        if not b:
            return None
        return to_board_type(b)
