import uuid

# Simulated in-memory user "database"
users = {}

def get_all_users():
    return list(users.values())

def create_user(data):
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
        "password": data.get("password")  # for now, plain text (we'll hash later)
    }
    users[user_id] = new_user
    return new_user

def get_user_by_id(user_id):
    return users.get(user_id)

def update_user(user_id, data):
    if user_id not in users:
        return None
    users[user_id].update(data)
    return users[user_id]

def delete_user(user_id):
    return users.pop(user_id, None)
