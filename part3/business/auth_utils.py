from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def admin_required(repo):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = repo.get("users", user_id)
            if not user or not user.get("is_admin", False):
                return jsonify({"msg": "Admins only"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
