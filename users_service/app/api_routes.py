from flask import Blueprint, jsonify
from .models import User

bp = Blueprint('api', __name__)

@bp.route('/user/<int:user_id>')
def get_user(user_id):
    """
    API endpoint to fetch user information by ID.
    Returns user details in JSON format.
    """
    user = User.query.get(user_id)

    if user: 
        return jsonify({
            'id': user.id, 
            'username': user.username,
            'email': user.email
        })
    else:
        return jsonify({'error': 'User not found'}), 404