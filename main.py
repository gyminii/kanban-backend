# 
# https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
# run command: uvicorn main:app --reload
import strawberry

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    @strawberry.field
    def hello() -> str:
        return "Hello, World!"

schema = strawberry.Schema(query=Query)

# FastAPI app
app = FastAPI()
graphql_app = GraphQLRouter(schema)
# Add GraphQL route
app.include_router(graphql_app, prefix="/graphql")


@app.get('/')

def read_root():
    return{ "message": 'Welcome'}
# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)