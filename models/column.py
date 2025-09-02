from typing import Optional, Dict, Any, List
from bson import ObjectId
from datetime import datetime
from db import columns_col

class ColumnModel:
    @staticmethod
    def by_id(column_id: str) -> Optional[Dict[str, Any]]:
        return columns_col.find_one({"_id": ObjectId(column_id)})

    @staticmethod
    def create(
        board_oid: ObjectId,
        title: str,
        order: int,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        now = datetime.now()
        doc: Dict[str, Any] = {
            "board_id": board_oid,
            "title": title,
            "order": order,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }
        columns_col.insert_one(doc)
        return doc

    @staticmethod
    def list_for_board(board_oid: ObjectId) -> List[Dict[str, Any]]:
        return list(columns_col.find({"board_id": board_oid}).sort("order", 1))

    @staticmethod
    def update_order(col_oid: ObjectId, new_order: int):
        columns_col.update_one({"_id": col_oid}, {"$set": {"order": new_order}})

    @staticmethod
    def update(col_oid: ObjectId, data: Dict[str, Any]):
        data["updated_at"] = datetime.now()
        columns_col.update_one({"_id": col_oid}, {"$set": data})

    @staticmethod
    def delete(col_oid: ObjectId) -> None:
        columns_col.delete_one({"_id": col_oid})

    @staticmethod
    def delete_for_board(board_oid: ObjectId) -> int:
        res = columns_col.delete_many({"board_id": board_oid})
        return getattr(res, "deleted_count", 0)

    @staticmethod
    def compact_orders(board_oid: ObjectId, removed_order: int) -> None:
        # Decrement order for all columns with order > removed_order
        columns_col.update_many(
            {"board_id": board_oid, "order": {"$gt": removed_order}},
            {"$inc": {"order": -1}}
        )
