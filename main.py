# 
# https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
# run command: uvicorn main:app --reload

import strawberry
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager


from schema import schema
from config import config
from services.mongodb_database import MongoDatabaseService

db_service = MongoDatabaseService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_service.connect()
    print("Connected to MongoDB")
    yield
    # Shutdown
    await db_service.disconnect()
    print("Disconnected from MongoDB")
    
# FastAPI app
app = FastAPI(
    title="Kanban Board API", 
    debug=config.DEBUG,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Add GraphQL route
app.include_router(graphql_app, prefix="/graphql")

@app.get('/')
def read_root():
    return {"message": "Kanban API is running"}

@app.get('/health')
def health_check():
    return {"status": "healthy", "service": "kanban-api"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=config.HOST, 
        port=config.PORT, 
        reload=config.DEBUG
    )
