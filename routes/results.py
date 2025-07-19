# routes/admin_results.py
from flask import Blueprint, jsonify
from database import get_db_connection
from scheduler import run_scheduling  # שים לב לשם הקובץ


results_bp = Blueprint('run-schedule', __name__)

@results_bp.route('/', methods=['POST'])
@results_bp.route('', methods=['POST'])
def run_schedule():
    conn = get_db_connection()
    constraints = conn.execute("SELECT user_id, shift_id, available_key FROM constraints")
    raw_data = [dict(zip(['user_id', 'shift_id', 'available_key'] , row)) for row in constraints.fetchall()]
    
    
    result = run_scheduling(raw_data)
    assignments = result['assignments']

    conn.execute("DELETE FROM result")

    for shift_id , user_ids in assignments.items():
        print("shift_id" , shift_id)
        print("user_ids" , user_ids)
        for user_id in user_ids:
           print("user_id" , type(user_id) , user_id)
           conn.execute("INSERT INTO result (shift_id , user_id) VALUES(? ,? )" ,  (shift_id , user_id))
    
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "assigned_shifts": assignments})
    
@results_bp.route("/" , methods=['GET'])
@results_bp.route("" , methods=['GET'])
def get_assigned_shifts():
    conn = get_db_connection()
    cursor = conn.cursor()

    # שליפת המידע הרלוונטי
    cursor.execute('''
        SELECT 
            r.shift_id,
            s.start_date,
            s.end_date,
            u.name
        FROM result r
        JOIN users u ON r.user_id = u.user_id
        JOIN shifts s ON r.shift_id = s.shift_id
        ORDER BY r.shift_id, u.name
    ''')

    rows = cursor.fetchall()
    conn.close()

    # ארגון המידע לפי shift_id
    from collections import defaultdict
    results_by_shift = defaultdict(lambda: {'shift_id': None, 'dates': '', 'users': []})

    for row in rows:
        shift_id = row['shift_id']
        if results_by_shift[shift_id]['shift_id'] is None:
            results_by_shift[shift_id]['shift_id'] = shift_id
            results_by_shift[shift_id]['dates'] = f"{row['start_date']} - {row['end_date']}"
        results_by_shift[shift_id]['users'].append(row['name'])

    # הפיכה לרשימה מוכנה ל-JSON
    results_list = list(results_by_shift.values())
    return jsonify(results_list)

