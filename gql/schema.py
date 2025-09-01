# gql/schema.py
import strawberry
from resolvers.queries.board import BoardQuery
from resolvers.mutations.board import BoardMutation
from resolvers.mutations.column import ColumnMutation
from resolvers.mutations.card import CardMutation
from resolvers.queries.card import CardQuery
@strawberry.type
class Query(BoardQuery, CardQuery):
    pass

@strawberry.type
class Mutation(BoardMutation, ColumnMutation, CardMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
