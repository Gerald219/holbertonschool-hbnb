from business.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False)
    places = db.relationship("Place", secondary="place_amenity", backref="amenities")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name", "")
