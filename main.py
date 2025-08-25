# app.py
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from strawberry.asgi import GraphQL
from gql.schema import schema
from utils.auth import get_user_id_from_request  # uses local JWT or remote Supabase

graphql_app = GraphQL(schema, debug=True)

app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

@app.route("/health")
async def health(_):
    return JSONResponse({"ok": True})
