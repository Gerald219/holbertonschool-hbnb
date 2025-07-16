from app.extensions import db
from business.base_model import BaseModel

class Review(BaseModel, db.Model):
    __tablename__ = "reviews"
    BaseModel.configure_fields(db)

    text = db.Column(db.String(1024), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey("places.id"), nullable=False)

    user = db.relationship("User", backref="reviews")
    place = db.relationship("Place", backref="reviews")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get("text", "")
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
