# models/board.py
from typing import Optional, Dict, Any, List
from bson import ObjectId
from datetime import datetime
from db import boards_col, columns_col

class BoardModel:
    @staticmethod
    def by_id(board_id: str) -> Optional[Dict[str, Any]]:
        return boards_col.find_one({"_id": ObjectId(board_id)})

    @staticmethod
    def list_for_user(user_id: str) -> List[Dict[str, Any]]:
        q = {"$or": [{"owner_id": user_id}, {"members": user_id}]}
        return list(boards_col.find(q).sort("updated_at", -1))

    @staticmethod
    def create(
        title: str,
        owner_id: str,
        description: Optional[str] = None,
        color: Optional[str] = None,            # e.g. "indigo", "#4f46e5"
        is_favorite: bool = False,
        is_archived: bool = False,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        now = datetime.utcnow()
        doc: Dict[str, Any] = {
            "title": title,
            "owner_id": owner_id,
            "members": [],
            "description": description,
            "color": color,
            "is_favorite": bool(is_favorite),
            "is_archived": bool(is_archived),
            "tags": tags or [],
            "created_at": now,
            "updated_at": now,
        }
        boards_col.insert_one(doc)
        return doc

    @staticmethod
    def update_fields(board_oid: ObjectId, data: Dict[str, Any]) -> Dict[str, Any]:
        # sanitize allowed fields only
        allowed = {"title", "description", "color", "is_favorite", "is_archived", "tags"}
        clean = {k: v for k, v in data.items() if k in allowed}
        if not clean:
            return boards_col.find_one({"_id": board_oid})
        clean["updated_at"] = datetime.utcnow()
        boards_col.update_one({"_id": board_oid}, {"$set": clean})
        return boards_col.find_one({"_id": board_oid})

    @staticmethod
    def add_member(board_id: str, member_user_id: str) -> Dict[str, Any]:
        boards_col.update_one(
            {"_id": ObjectId(board_id)},
            {"$addToSet": {"members": member_user_id}, "$set": {"updated_at": datetime.utcnow()}}
        )
        return boards_col.find_one({"_id": ObjectId(board_id)})

    @staticmethod
    def column_count(board_oid: ObjectId) -> int:
        return columns_col.count_documents({"board_id": board_oid})
