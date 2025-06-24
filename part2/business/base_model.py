import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        result = self.__dict__.copy()
        return result

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow().isoformat()
