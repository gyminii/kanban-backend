# resolvers/queries/card.py
import strawberry
from typing import List, Optional
from models.card import CardModel
from utils.serialize import to_card_type
from gql.types import Card

@strawberry.type
class CardQuery:
    @strawberry.field
    def get_cards(self, user_id: str, board_id: Optional[str] = None) -> List[Card]:
        docs = CardModel.list_for_user(user_id=user_id, board_id=board_id)
        return [to_card_type(doc) for doc in docs]