from .base import BaseRepository
from ..extensions import db

class SQLAlchemyRepository(BaseRepository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def list(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.model.query.get(obj_id)
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.model.query.get(obj_id)
        db.session.delete(obj)
        db.session.commit()
