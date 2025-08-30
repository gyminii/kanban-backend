# resolvers/queries/column.py
import strawberry
from typing import Optional
from strawberry.types import Info

from models import ColumnModel
from utils.serialize import to_column_type
from gql.types import Column

@strawberry.type
class Query:
    @strawberry.field
    def column(self, info: Info, column_id: strawberry.ID) -> Optional[Column]:
        c = ColumnModel.by_id(str(column_id))
        if not c:
            return None
        return to_column_type(c)
