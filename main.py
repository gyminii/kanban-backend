# app.py
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse
from strawberry.asgi import GraphQL
from gql.schema import schema

graphql_app = GraphQL(schema, debug=True)

# uvicorn main:app --reload --host 0.0.0.0 --port 8080
app = Starlette()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)
# Redirecting to /graphql from root.
@app.route("/")
async def root(_):
    return RedirectResponse(url="/graphql")
# Grphql playground
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

@app.route("/health")
async def health(_):
    return JSONResponse({"ok": True})
