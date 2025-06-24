import uuid
from datetime import datetime

class InMemoryRepository:
    def __init__(self):
        self.storage = {
            "users": {},
            "places": {},
            "reviews": {},
            "amenities": {}
        }

    def generate_id(self):
        return str(uuid.uuid4())

    def save(self, entity_type, data):
        entity_id = self.generate_id()
        data["id"] = entity_id
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()
        self.storage[entity_type][entity_id] = data
        return data

    def get(self, entity_type, entity_id):
        return self.storage[entity_type].get(entity_id)

    def get_all(self, entity_type):
        return list(self.storage[entity_type].values())

    def update(self, entity_type, entity_id, updates):
        entity = self.storage[entity_type].get(entity_id)
        if entity:
            entity.update(updates)
            entity["updated_at"] = datetime.utcnow().isoformat()
            return entity
        return None

    def delete(self, entity_type, entity_id):
        return self.storage[entity_type].pop(entity_id, None)
