from business.base_model import BaseModel
from app.extensions import db

class Place(BaseModel):
    __tablename__ = 'places'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(128), nullable=False)
    number_rooms = db.Column(db.Integer, default=0)
    number_bathrooms = db.Column(db.Integer, default=0)
    max_guest = db.Column(db.Integer, default=0)
    price_by_night = db.Column(db.Integer, default=0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    reviews = db.relationship('Review', backref='place', lazy=True)
    
    amenities = db.relationship(
        'Amenity',
        secondary='place_amenity',
        backref='places',
        lazy=True
    )
