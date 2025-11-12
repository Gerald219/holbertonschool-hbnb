from __future__ import annotations
from typing import Dict, Any, Optional, List
from part3.app.extensions import db
from part3.models import Review, Place

def _to_dict(r: Review) -> Dict[str, Any]:
    return {
        "id": r.id,
        "text": r.text,
        "user_id": r.user_id,
        "place_id": r.place_id,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "updated_at": r.updated_at.isoformat() if r.updated_at else None,
    }

def list_reviews() -> List[Dict[str, Any]]:
    rows = Review.query.order_by(Review.created_at.asc()).all()
    return [_to_dict(r) for r in rows]

def get_review(review_id: str) -> Optional[Dict[str, Any]]:
    r = db.session.get(Review, review_id)
    return _to_dict(r) if r else None

def create_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    # expects: text, place_id, user_id
    text = (payload.get("text") or "").strip()
    place_id = payload.get("place_id")
    user_id = payload.get("user_id")

    if not text or not place_id or not user_id:
        raise ValueError("missing_required_fields")

    # place must exist
    place = db.session.get(Place, place_id)
    if not place:
        raise ValueError("place_not_found")

    # no self-review
    if place.owner_id == user_id:
        raise ValueError("self_review_forbidden")

    # one review per user per place
    existing = Review.query.filter_by(user_id=user_id, place_id=place_id).first()
    if existing:
        raise ValueError("duplicate_review")

    r = Review(text=text, place_id=place_id, user_id=user_id)
    db.session.add(r)
    db.session.commit()
    return _to_dict(r)

def update_review(review_id: str, updates: Dict[str, Any], *, actor_id: str) -> Optional[Dict[str, Any]]:
    # author-only edit (only 'text')
    r = db.session.get(Review, review_id)
    if not r:
        return None
    if r.user_id != actor_id:
        raise ValueError("forbidden_not_author")
    if "text" not in updates or updates["text"] is None:
        raise ValueError("nothing_to_update")
    r.text = (updates["text"] or "").strip()
    db.session.commit()
    return _to_dict(r)

def delete_review(review_id: str, *, actor_id: str, is_admin: bool) -> bool:
    # author OR admin can delete
    r = db.session.get(Review, review_id)
    if not r:
        return False
    if not (is_admin or r.user_id == actor_id):
        raise ValueError("forbidden_delete")
    db.session.delete(r)
    db.session.commit()
    return True
