from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    def to_dict(self):
        data = {}
        for col in self.__table__.columns:
            if col.name == 'password':
                continue
            data[col.name] = getattr(self, col.name)
        return data
