from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # מאפשר גישה מה-frontend

# יצירת טבלה אם לא קיימת
def init_db():
    with sqlite3.connect("todos.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )''')

init_db()

# שליפת כל הפריטים
@app.route("/todos", methods=["GET"])
def get_todos():
    with sqlite3.connect("todos.db") as conn:
        rows = conn.execute("SELECT id, text FROM todos").fetchall()
        return jsonify([{"id": r[0], "text": r[1]} for r in rows])

# הוספת פריט חדש
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    with sqlite3.connect("todos.db") as conn:
        cur = conn.execute("INSERT INTO todos (text) VALUES (?)", (data["text"],))
        conn.commit()
        return jsonify({"id": cur.lastrowid, "text": data["text"]}), 201

# עריכת פריט קיים
@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    with sqlite3.connect("todos.db") as conn:
        conn.execute("UPDATE todos SET text=? WHERE id=?", (data["text"], id))
        conn.commit()
        return jsonify({"id": id, "text": data["text"]})

# מחיקת פריט
@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    with sqlite3.connect("todos.db") as conn:
        conn.execute("DELETE FROM todos WHERE id=?", (id,))
        conn.commit()
        return '', 204

if __name__ == "__main__":
    app.run(debug=True)
