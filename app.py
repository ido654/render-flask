# app.py
from flask import Flask
from flask_cors import CORS
from flask import request


from models import init_db
from routes.users import users_bp
from routes.shifts import shifts_bp
from routes.constraints import constraints_bp
from routes.results import results_bp

app = Flask(__name__)


init_db()

# רישום מסלולים
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(shifts_bp, url_prefix='/api/shifts')
app.register_blueprint(constraints_bp, url_prefix='/api/constraints')
app.register_blueprint(results_bp , url_prefix= '/api/run-schedule')

CORS(app,
     supports_credentials=True,
     resources={r"/api/*": {"origins": ["http://10.0.0.12:3000" , 'http://localhost:3000']}},
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
