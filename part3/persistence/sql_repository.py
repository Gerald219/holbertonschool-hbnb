# part3/persistence/sql_repository.py
from __future__ import annotations
from typing import Dict, Any, List, Optional
from sqlalchemy import select
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
    rows = db.session.execute(select(User).order_by(User.created_at.asc())).scalars().all()
    return [user_to_dict(u) for u in rows]

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    u = db.session.get(User, user_id)
    return user_to_dict(u) if u else None

def get_user_row_by_email(email: str) -> Optional[User]:
    return db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()


def create_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    first = payload.get("first_name")
    last  = payload.get("last_name")
    email = payload.get("email")
    pw    = payload.get("password")

    if not all([first, last, email, pw]):
        raise ValueError("missing_fields")

    
    if get_user_row_by_email(email):
        raise ValueError("email_already_exists")

    hashed = bcrypt.generate_password_hash(pw).decode("utf-8")
    u = User(first_name=first, last_name=last, email=email)
    u.password_hash = hashed

    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        # unique index fallback
        raise ValueError("email_already_exists")

    return user_to_dict(u)

def update_user(user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    u = db.session.get(User, user_id)
    if not u:
        return None

    
    first = updates.get("first_name", u.first_name)
    last  = updates.get("last_name",  u.last_name)
    email = updates.get("email",      u.email)

    if email != u.email and get_user_row_by_email(email):
        raise ValueError("email_already_exists")

    u.first_name = first
    u.last_name  = last
    u.email      = email

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("email_already_exists")

    return user_to_dict(u)

def delete_user(user_id: str) -> bool:
    u = db.session.get(User, user_id)
    if not u:
        return False
    db.session.delete(u)
    db.session.commit()
    return True
