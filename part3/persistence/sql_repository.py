from __future__ import annotations
from typing import Optional, Dict, Any, List
from sqlalchemy.exc import IntegrityError
from part3.app.extensions import db, bcrypt
from part3.models import User

def user_to_dict(u: User) -> Dict[str, Any]:
    return {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "updated_at": u.updated_at.isoformat() if u.updated_at else None,
    }

def list_users() -> List[Dict[str, Any]]:
    return [user_to_dict(u) for u in User.query.order_by(User.created_at.asc()).all()]

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    u = db.session.get(User, user_id)
    return user_to_dict(u) if u else None

def create_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    first = payload.get("first_name"); last  = payload.get("last_name")
    email = payload.get("email");      pw    = payload.get("password")
    if not all([first, last, email, pw]):
        raise ValueError("Missing required fields: first_name, last_name, email, password")
    hashed = bcrypt.generate_password_hash(pw).decode("utf-8")
    u = User(first_name=first, last_name=last, email=email, password_hash=hashed)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Email already exists")
    return user_to_dict(u)

def update_user(user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    u = db.session.get(User, user_id)
    if not u:
        return None
    allowed = {"first_name", "last_name", "email"}
    for k in list(updates.keys()):
        if k not in allowed:
            updates.pop(k, None)
    for k, v in updates.items():
        setattr(u, k, v)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Email already exists")
    return user_to_dict(u)

def delete_user(user_id: str) -> bool:
    u = db.session.get(User, user_id)
    if not u:
        return False
    db.session.delete(u)
    db.session.commit()
    return True
