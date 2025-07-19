# routes/shifts.py
from flask import Blueprint, request, jsonify
from database import get_db_connection

shifts_bp = Blueprint('shifts', __name__)

@shifts_bp.route('/', methods=['GET'])
@shifts_bp.route('', methods=['GET'])
def get_shifts():
    conn = get_db_connection()
    shifts = conn.execute('SELECT * FROM shifts').fetchall()
    conn.close()
    return jsonify([dict(s) for s in shifts])

@shifts_bp.route('/', methods=['POST'])
@shifts_bp.route('', methods=['POST'])
def add_shift():
    data = request.json
    start = data.get('start_date')
    end = data.get('end_date')
    if not start or not end:
        return jsonify({'error': 'start_date and end_date are required'}), 400
    conn = get_db_connection()
    conn.execute('INSERT INTO shifts (start_date, end_date) VALUES (?, ?)', (start, end))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Shift added'}), 201

@shifts_bp.route("/<int:shift_id>" , methods=['PUT'])
@shifts_bp.route("/<int:shift_id>/" , methods=['PUT'])
def uodate_shift(shift_id):
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    conn = get_db_connection()
    conn.execute('UPDATE shifts SET start_date = ?, end_date = ? WHERE shift_id = ?', (start_date, end_date, shift_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Shift updated'})


@shifts_bp.route('/<int:shift_id>', methods=['DELETE'])
@shifts_bp.route('/<int:shift_id>/', methods=['DELETE'])
def delete_shift(shift_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM shifts WHERE shift_id = ?', (shift_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Shift deleted'})
