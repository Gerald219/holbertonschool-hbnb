# part3/persistence/user_storage.py
from .repository import InMemoryRepository

# One shared in-memory repo for the whole app (users, auth, etc.)
repo = InMemoryRepository()
