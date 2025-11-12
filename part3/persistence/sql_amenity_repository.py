from __future__ import annotations
from typing import Dict, Any, Optional, List
from part3.app.extensions import db
from part3.models import Amenity

def _to_dict(a: Amenity) -> Dict[str, Any]:
    return {
        "id": a.id,
        "name": a.name,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
    }

def list_amenities() -> List[Dict[str, Any]]:
    rows = Amenity.query.order_by(Amenity.created_at.asc()).all()
    return [_to_dict(a) for a in rows]

def get_amenity(amenity_id: str) -> Optional[Dict[str, Any]]:
    a = db.session.get(Amenity, amenity_id)
    return _to_dict(a) if a else None

def create_amenity(payload: Dict[str, Any]) -> Dict[str, Any]:
    a = Amenity(name=payload["name"])
    db.session.add(a)
    db.session.commit()
    return _to_dict(a)

def update_amenity(amenity_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    a = db.session.get(Amenity, amenity_id)
    if not a:
        return None
    if "name" in updates and updates["name"] is not None:
        a.name = updates["name"]
    db.session.commit()
    return _to_dict(a)

def delete_amenity(amenity_id: str) -> bool:
    a = db.session.get(Amenity, amenity_id)
    if not a:
        return False
    db.session.delete(a)
    db.session.commit()
    return True
