# utils/dnd.py
from db import cards_col, columns_col
from bson import ObjectId

def clamp(n: int, low: int, high: int) -> int:
    return max(low, min(high, n))

def reorder_within_column(col_oid: ObjectId, old_order: int, new_order: int):
    if new_order == old_order:
        return
    if new_order < old_order:
        # moving up
        cards_col.update_many(
            {"column_id": col_oid, "order": {"$gte": new_order, "$lt": old_order}},
            {"$inc": {"order": 1}}
        )
    else:
        # moving down
        cards_col.update_many(
            {"column_id": col_oid, "order": {"$lte": new_order, "$gt": old_order}},
            {"$inc": {"order": -1}}
        )

def remove_gap_in_column(col_oid: ObjectId, removed_order: int):
    cards_col.update_many(
        {"column_id": col_oid, "order": {"$gt": removed_order}},
        {"$inc": {"order": -1}}
    )

def make_space_in_column(col_oid: ObjectId, at_order: int):
    cards_col.update_many(
        {"column_id": col_oid, "order": {"$gte": at_order}},
        {"$inc": {"order": 1}}
    )

def reorder_columns_within_board(board_oid: ObjectId, old_order: int, new_order: int):
    if new_order == old_order:
        return
    if new_order < old_order:
        columns_col.update_many(
            {"board_id": board_oid, "order": {"$gte": new_order, "$lt": old_order}},
            {"$inc": {"order": 1}}
        )
    else:
        columns_col.update_many(
            {"board_id": board_oid, "order": {"$lte": new_order, "$gt": old_order}},
            {"$inc": {"order": -1}}
        )
