# app.py
from flask import Flask
from flask_cors import CORS
from flask import request


from models import init_db
from routes.users import users_bp
from routes.shifts import shifts_bp
from routes.constraints import constraints_bp

app = Flask(__name__)

CORS(app, supports_credentials=True,
     origins=["http://localhost:3000" , "daharis-todos-app.netlify.app"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])


init_db()

# רישום מסלולים
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(shifts_bp, url_prefix='/api/shifts')
app.register_blueprint(constraints_bp, url_prefix='/api/constraints')

if __name__ == '__main__':
    app.run(debug=True ,host='localhost', port=5000)
