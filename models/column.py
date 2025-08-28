# models/column.py
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
        status: Optional[str] = None,  # e.g. "active" | "planned" | "completed"
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