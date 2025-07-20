from flask import Blueprint, jsonify

places_bp = Blueprint('places', __name__, url_prefix='/api/v1/places')

@places_bp.route('/', methods=['GET'])
def list_places():
    return jsonify({'status': 'ok'})
