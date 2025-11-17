from __future__ import annotations
from typing import Dict, Any, Optional, List

from sqlalchemy.exc import IntegrityError
from part3.app.extensions import db, bcrypt
from part3.models import User


class SQLAlchemyRepository:
    def _to_dict(self, u: User) -> Dict[str, Any]:
        return {
            "id": u.id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "updated_at": u.updated_at.isoformat() if u.updated_at else None,
        }

    # ---------- READ ----------
    def list_users(self) -> List[Dict[str, Any]]:
        users = User.query.order_by(User.created_at.asc()).all()
        return [self._to_dict(u) for u in users]

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        u = db.session.get(User, user_id)
        return self._to_dict(u) if u else None

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        first = (payload.get("first_name") or "").strip()
        last  = (payload.get("last_name") or "").strip()
        email = (payload.get("email") or "").strip()
        pw    = payload.get("password")

        if not first or not last or not email or not pw:
            raise ValueError("missing_required_fields")

        u = User(first_name=first, last_name=last, email=email)
        u.password_hash = bcrypt.generate_password_hash(pw).decode("utf-8")

        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            # Only map to duplicate email if the DB says so
            text = str(getattr(e, "orig", e)).lower()
            if "unique" in text and "email" in text:
                raise ValueError("email_already_exists")
            raise  # Raise other unexpected integrity errors

        return self._to_dict(u)

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        u = db.session.get(User, user_id)
        if not u:
            return None

        for key in ("first_name", "last_name", "email"):
            if key in updates and updates[key] is not None:
                setattr(u, key, updates[key])

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            text = str(getattr(e, "orig", e)).lower()
            if "unique" in text and "email" in text:
                raise ValueError("email_already_exists")
            raise

        return self._to_dict(u)

    def delete_user(self, user_id: str) -> bool:
        u = db.session.get(User, user_id)
        if not u:
            return False
        db.session.delete(u)
        db.session.commit()
        return True

