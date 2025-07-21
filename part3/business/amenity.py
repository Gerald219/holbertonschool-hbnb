from business.base_model import BaseModel
from app.extensions import db
from business.place import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    places = db.relationship(
        'Place',
        secondary=place_amenity,
        back_populates='amenities',
        lazy='dynamic'
    )
