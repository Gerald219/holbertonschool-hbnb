from __future__ import annotations
from typing import Dict, Any, Optional, List
from part3.app.extensions import db
from part3.models import Place, Amenity

def _to_dict(p: Place) -> Dict[str, Any]:
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "city": p.city,
        "price_per_night": p.price_per_night,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "owner_id": p.owner_id,
        "amenity_ids": [a.id for a in (p.amenities or [])],
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }

def list_places() -> List[Dict[str, Any]]:
    rows = Place.query.order_by(Place.created_at.asc()).all()
    return [_to_dict(p) for p in rows]

def get_place(place_id: str) -> Optional[Dict[str, Any]]:
    p = db.session.get(Place, place_id)
    return _to_dict(p) if p else None

def create_place(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Validate price_per_night
    if not payload.get("price_per_night") or not isinstance(
        payload["price_per_night"], int
    ) or payload["price_per_night"] <= 0:
        raise ValueError("invalid_value: price_per_night")

    # Validate latitude and longitude
    if "latitude" in payload and not isinstance(
        payload["latitude"], (float, int)
    ):
        raise ValueError("invalid_value: latitude")
    if "longitude" in payload and not isinstance(
        payload["longitude"], (float, int)
    ):
        raise ValueError("invalid_value: longitude")

    # Create place
    p = Place(
        name=payload["name"],
        city=payload["city"],
        price_per_night=payload["price_per_night"],
        description=payload.get("description"),
        latitude=payload.get("latitude"),
        longitude=payload.get("longitude"),
        owner_id=payload["owner_id"],
    )

    # Add and commit to the database
    db.session.add(p)
    db.session.commit()

    # Return the created place as a dictionary
    return _to_dict(p)




def update_place(place_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    p = db.session.get(Place, place_id)
    if not p:
        return None
    for key in ("name", "city", "price_per_night", "description", "latitude", "longitude"):
        if key in updates:
            setattr(p, key, updates[key])
    db.session.commit()
    return _to_dict(p)

def attach_amenity(place_id: str, amenity_id: str) -> Optional[Dict[str, Any]]:
    p = db.session.get(Place, place_id)
    a = db.session.get(Amenity, amenity_id)
    if not p or not a:
        return None
    if a not in p.amenities:
        p.amenities.append(a)
        db.session.commit()
    return _to_dict(p)

def detach_amenity(place_id: str, amenity_id: str) -> Optional[Dict[str, Any]]:
    p = db.session.get(Place, place_id)
    a = db.session.get(Amenity, amenity_id)
    if not p or not a:
        return None
    if a in p.amenities:
        p.amenities.remove(a)
        db.session.commit()
    return _to_dict(p)

def delete_place(place_id: str) -> bool:
    """Delete a place by id. Return True if deleted, False if not found."""
    place = db.session.get(Place, place_id)
    if not place:
        return False

    db.session.delete(place)
    db.session.commit()
    return True

