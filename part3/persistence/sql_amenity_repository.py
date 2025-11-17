from __future__ import annotations
from typing import Dict, Any, Optional, List
from part3.app.extensions import db
from business.facade import Facade  # Import the Facade class

# Instantiate the Facade
facade = Facade()

def _to_dict(a: Amenity) -> Dict[str, Any]:
    return {
        "id": a.id,
        "name": a.name,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
    }

def list_amenities() -> List[Dict[str, Any]]:
    return facade.list_amenities()  # Use the Facade method

def get_amenity(amenity_id: str) -> Optional[Dict[str, Any]]:
    return facade.get_amenity(amenity_id)  # Use the Facade method

def create_amenity(payload: Dict[str, Any]) -> Dict[str, Any]:
    return facade.create_amenity(payload)  # Use the Facade method

def update_amenity(amenity_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return facade.update_amenity(amenity_id, updates)  # Use the Facade method

def delete_amenity(amenity_id: str) -> bool:
    return facade.delete_amenity(amenity_id)  # Use the Facade method

