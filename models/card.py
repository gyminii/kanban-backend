from typing import Optional, Dict, Any, List
from bson import ObjectId
from db import cards_col
from datetime import datetime

import db

class CardModel:
    @staticmethod
    def by_id(card_id: str) -> Optional[Dict[str, Any]]:
        return cards_col.find_one({"_id": ObjectId(card_id)})

    @staticmethod
    def create(
        board_oid: ObjectId,
        column_oid: ObjectId,
        title: str,
        description: Optional[str],
        order: int,
        assigned_to: Optional[str] = None,
        due_date: Optional[datetime] = None, 
        completed: bool = False,  
        tags: Optional[List[str]] = None, 
    ) -> Dict[str, Any]:
        from datetime import datetime
        now = datetime.now()
        doc = {
            "board_id": board_oid,
            "column_id": column_oid,
            "title": title,
            "description": description,
            "order": order,
            "assigned_to": assigned_to,
            "created_at": now,
            "updated_at": now,
            "due_date": due_date,
            "completed": completed,
            "archived": False, 
            "tags": tags or [], 
        }
        cards_col.insert_one(doc)
        return doc

    @staticmethod
    def list_for_column(col_oid: ObjectId) -> List[Dict[str, Any]]:
        return list(cards_col.find({"column_id": col_oid}).sort("order", 1))
    @staticmethod
    def list_for_user(user_id: str, board_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {}
        if board_id:
            query["board_id"] = ObjectId(board_id)
        else:
            query = {}

        return list(cards_col.find(query).sort("updated_at", -1))

    @staticmethod
    def count_in_column(col_oid: ObjectId) -> int:
        return cards_col.count_documents({"column_id": col_oid})

    @staticmethod
    def update(card_oid: ObjectId, data: Dict[str, Any]) -> None:
        data["updated_at"] = datetime.now() 
        cards_col.update_one({"_id": card_oid}, {"$set": data})

    # --- NEW: delete a single card ---
    @staticmethod
    def delete(card_oid: ObjectId) -> None:
        cards_col.delete_one({"_id": card_oid})

    # --- NEW: bulk delete all cards for a column; returns count ---
    @staticmethod
    def delete_in_column(col_oid: ObjectId) -> int:
        res = cards_col.delete_many({"column_id": col_oid})
        return getattr(res, "deleted_count", 0)
