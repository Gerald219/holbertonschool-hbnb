from business.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.city = kwargs.get("city", "")
        self.price_per_night = kwargs.get("price_per_night", 0)
        self.latitude = kwargs.get("latitude", 0.0)
        self.longitude = kwargs.get("longitude", 0.0)
        self.owner_id = kwargs.get("owner_id", "")
        self.amenity_ids = kwargs.get("amenity_ids", [])
        super().__init__(**kwargs)
