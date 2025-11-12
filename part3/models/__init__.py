from uuid import uuid4
from datetime import datetime
from part3.app.extensions import db

def _uuid() -> str:
    return str(uuid4())

def _utcnow() -> datetime:
    return datetime.utcnow()


place_amenities = db.Table(
    "place_amenities",
    db.Column("place_id",  db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
)

class TimestampMixin(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=_utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

class User(TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=_uuid)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


    places  = db.relationship("Place",  back_populates="owner",  cascade="all, delete-orphan", lazy="selectin")
    reviews = db.relationship("Review", back_populates="author", cascade="all, delete-orphan", lazy="selectin")

class Place(TimestampMixin):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=_uuid)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    owner = db.relationship("User", back_populates="places", lazy="selectin")  # optional selectin

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenities,
        back_populates="places",
        lazy="selectin",
    )

    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan", lazy="selectin")

class Amenity(TimestampMixin):
    __tablename__ = "amenities"

    id = db.Column(db.String(36), primary_key=True, default=_uuid)
    name = db.Column(db.String, unique=True, nullable=False)

    places = db.relationship(
        "Place",
        secondary=place_amenities,
        back_populates="amenities",
        lazy="selectin",  # optional selectin
    )

class Review(TimestampMixin):
    __tablename__ = "reviews"

    id = db.Column(db.String(36), primary_key=True, default=_uuid)
    text = db.Column(db.Text, nullable=False)

    user_id  = db.Column(db.String(36), db.ForeignKey("users.id"),  nullable=False, index=True)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False, index=True)

    author = db.relationship("User",  back_populates="reviews", lazy="selectin")  # optional selectin
    place  = db.relationship("Place", back_populates="reviews", lazy="selectin")  # optional selectin
