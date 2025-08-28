# resolvers/mutations/board.py

import strawberry
from typing import Optional, List
from strawberry.types import Info

from models import BoardModel
from utils.serialize import to_board_type
from gql.types import Board


@strawberry.type
class BoardMutation:
    @strawberry.mutation
    def create_board(
        self,
        info: Info,
        title: str,
        owner_id: str,
        description: Optional[str] = None,
        color: Optional[str] = None,
        is_favorite: Optional[bool] = False,
        is_archived: Optional[bool] = False,
        tags: Optional[List[str]] = None,
    ) -> Board:
        b = BoardModel.create(
            title=title,
            owner_id=owner_id,
            description=description,
            color=color,
            is_favorite=is_favorite,
            is_archived=is_archived,
            tags=tags,
        )
        return to_board_type(b)

    @strawberry.mutation
    def update_board(
        self,
        info: Info,
        board_id: strawberry.ID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        is_archived: Optional[bool] = None,
        tags: Optional[List[str]] = None,
    ) -> Board:
        b = BoardModel.by_id(str(board_id))
        if not b:
            raise Exception("Board not found")

        # Build update dict dynamically in one shot
        input_data = {
            "title": title,
            "description": description,
            "color": color,
            "is_favorite": is_favorite,
            "is_archived": is_archived,
            "tags": tags,
        }

        # Drop None values only
        data = {k: v for k, v in input_data.items() if v is not None}

        updated = BoardModel.update_fields(b["_id"], data)
        return to_board_type(updated)

    @strawberry.mutation
    def invite_member(self, info: Info, board_id: strawberry.ID, member_user_id: str) -> Board:
        b = BoardModel.by_id(str(board_id))
        if not b:
            raise Exception("Board not found")
        updated = BoardModel.add_member(str(board_id), member_user_id)
        return to_board_type(updated)
