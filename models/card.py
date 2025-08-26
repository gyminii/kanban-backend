# models/card.py
from typing import Optional, Dict, Any, List
from bson import ObjectId
from db import cards_col
from datetime import datetime

class CardModel:
    @staticmethod
    def by_id(card_id: str) -> Optional[Dict[str, Any]]:
        return cards_col.find_one({"_id": ObjectId(card_id)})

    @staticmethod
    def create(
        column_oid: ObjectId,
        title: str,
        description: Optional[str],
        order: int,
        assigned_to: Optional[str] = None,
        due_date: Optional[datetime] = None, 
        completed: bool = False,  
    ) -> Dict[str, Any]:
        from datetime import datetime
        now = datetime.now()
        doc = {
            "column_id": column_oid,
            "title": title,
            "description": description,
            "order": order,
            "assigned_to": assigned_to,
            "created_at": now,
            "updated_at": now,
            "due_date": due_date,
            "completed": completed,
        }
        cards_col.insert_one(doc)
        return doc

    @staticmethod
    def list_for_column(col_oid: ObjectId) -> List[Dict[str, Any]]:
        return list(cards_col.find({"column_id": col_oid}).sort("order", 1))

    @staticmethod
    def count_in_column(col_oid: ObjectId) -> int:
        return cards_col.count_documents({"column_id": col_oid})

    @staticmethod
    def update(card_oid: ObjectId, data: Dict[str, Any]) -> None:
        data["updated_at"] = datetime.now() 
        cards_col.update_one({"_id": card_oid}, {"$set": data})
