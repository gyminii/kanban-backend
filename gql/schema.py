# gql/schema.py
import strawberry
from resolvers.queries.board import Query as BoardQuery
from resolvers.mutations.board import BoardMutation
from resolvers.mutations.column import ColumnMutation
from resolvers.mutations.card import CardMutation

@strawberry.type
class Query(BoardQuery):
    pass

@strawberry.type
class Mutation(BoardMutation, ColumnMutation, CardMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
