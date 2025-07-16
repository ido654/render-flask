# routes/constraints.py
from flask import Blueprint, request, jsonify
from database import get_db_connection

constraints_bp = Blueprint('constraints', __name__)

@constraints_bp.route('/', methods=['GET'])
def get_constraints():
    conn = get_db_connection()
    constraints = conn.execute('SELECT * FROM constraints').fetchall()
    conn.close()
    return jsonify([dict(c) for c in constraints])

@constraints_bp.route('/<int:user_id>/<int:shift_id>', methods=['PATCH'])
def update_constraint(user_id, shift_id):
    data = request.json
    key = data.get('available_key')
    if key not in (0, 1 , 2):
        return jsonify({'error': 'available_key must be 0 or 1 or 2'}), 400
    conn = get_db_connection()
    conn.execute('''
        UPDATE constraints SET available_key = ?
        WHERE user_id = ? AND shift_id = ?
    ''', (key, user_id, shift_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Constraint updated'})
