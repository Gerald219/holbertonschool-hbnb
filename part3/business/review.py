from business.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, **kwargs):
        self.text = kwargs.get("text", "")
        self.user_id = kwargs.get("user_id", "")
        self.place_id = kwargs.get("place_id", "")
        super().__init__(**kwargs)
