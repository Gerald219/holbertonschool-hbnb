from __future__ import annotations
from typing import Dict, Any, List, Optional

from sqlalchemy.exc import IntegrityError
from part3.app.extensions import db, bcrypt
from part3.models import User


def _to_dict(u: User) -> Dict[str, Any]:
    return {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "updated_at": u.updated_at.isoformat() if u.updated_at else None,
    }


def list_users() -> List[Dict[str, Any]]:
    users = User.query.order_by(User.created_at.asc()).all()
    return [_to_dict(u) for u in users]


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    u = db.session.get(User, user_id)
    return _to_dict(u) if u else None


def create_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    first = payload.get("first_name")
    last  = payload.get("last_name")
    email = payload.get("email")
    pw    = payload.get("password")
    if not all([first, last, email, pw]):
        raise ValueError("missing required fields: first_name, last_name, email, password")

    hashed = bcrypt.generate_password_hash(pw).decode("utf-8")

    
    u = User(first_name=first, last_name=last, email=email)
    u.password_hash = hashed

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        raise ValueError("email_already_exists")

    return _to_dict(u)


def update_user(user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    u = db.session.get(User, user_id)
    if not u:
        return None

    
    for key in ("first_name", "last_name", "email"):
        if key in updates and updates[key] is not None:
            setattr(u, key, updates[key])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("email_already_exists")

    return _to_dict(u)


def delete_user(user_id: str) -> bool:
    u = db.session.get(User, user_id)
    if not u:
        return False
    db.session.delete(u)
    db.session.commit()
    return True
