from business.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        super().__init__(**kwargs)
