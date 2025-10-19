from business.user import User
from business.place import Place
from business.review import Review
from business.amenity import Amenity

user = User(first_name="Gerald", last_name="Mulero", email="gerald@example.com", password="1234")
place = Place(name="Beach House", city="San Juan", price_per_night=120, owner_id=user.id)
amenity = Amenity(name="WiFi")
review = Review(text="Loved this place!", user_id=user.id, place_id=place.id)

print("User:", user.to_dict())
print("Place:", place.to_dict())
print("Amenity:", amenity.to_dict())
print("Review:", review.to_dict())
