import certifi

from pymongo import MongoClient, errors
from config import app_config

MONGO_URI = app_config.DATABASE_URL
if not MONGO_URI:
    raise RuntimeError("MONGO_URI env var missing")

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    # Force connection check
    print("Connected to MongoDB")
except errors.ServerSelectionTimeoutError as e:
    print("Could not connect to MongoDB", e)
    raise

db = client["kanban"]

boards_col = db["boards"]
columns_col = db["columns"]
cards_col = db["cards"]

# Helpful indexes
boards_col.create_index([("owner_id", 1)])
boards_col.create_index([("members", 1)])
columns_col.create_index([("board_id", 1), ("order", 1)])
cards_col.create_index([("column_id", 1), ("order", 1)])
