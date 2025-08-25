# resolvers/mutations/board.py
import strawberry
from strawberry.types import Info

from models import BoardModel
from utils.serialize import to_board_type
from utils.auth import require_user
from gql.types import Board  # <-- import

@strawberry.type
class BoardMutation:
    @strawberry.mutation
    def create_board(self, info: Info, title: str) -> Board:
        user_id = require_user(info) 
        b = BoardModel.create(title, user_id)
        return to_board_type(b)

    @strawberry.mutation
    def invite_member(self, info: Info, board_id: strawberry.ID, member_user_id: str) -> Board:
        user_id = require_user(info)
        b = BoardModel.by_id(str(board_id))
        if not b:
            raise Exception("Board not found")
        if b["owner_id"] != user_id:
            raise Exception("Only owner can invite")
        updated = BoardModel.add_member(str(board_id), member_user_id)
        return to_board_type(updated)
