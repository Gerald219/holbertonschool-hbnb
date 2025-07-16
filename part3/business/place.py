from app.extensions import db
from business.base_model import BaseModel
from datetime import datetime

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel, db.Model):
    __tablename__ = "places"
    BaseModel.configure_fields(db)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    city = db.Column(db.String(128))
    price_per_night = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship("User", backref="places")
    reviews = db.relationship("Review", backref="place", cascade="all, delete")
    amenities = db.relationship("Amenity", secondary=place_amenity, backref="places")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.city = kwargs.get("city", "")
        self.price_per_night = kwargs.get("price_per_night", 0)
        self.latitude = kwargs.get("latitude", 0.0)
        self.longitude = kwargs.get("longitude", 0.0)
        self.owner_id = kwargs.get("owner_id", "")

