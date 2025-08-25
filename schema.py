"""
Main GraphQL schema composition
"""

import strawberry
from resolvers import (
    BoardQueries,
    BoardMutations,
    ListMutations,
    CardQueries,
    CardMutations
)

# @strawberry.type
# class Query(AuthQueries, BoardQueries, CardQueries):
#     """Combined query class with all domain queries"""
#     pass

@strawberry.type
class Mutation(AuthMutations, BoardMutations, ListMutations, CardMutations):
    """Combined mutation class with all domain mutations"""
    pass

# Create the main GraphQL schema
schema = strawberry.Schema(
    # query=Query,
    mutation=Mutation
)


# import strawberry
# from resolvers.auth_queries import AuthQueries

# @strawberry.type
# class Query(AuthQueries):
#     """Combined query class with auth queries only"""
#     pass

# # Create minimal schema with just queries first
# schema = strawberry.Schema(query=Query)