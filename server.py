from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="client/build", static_url_path="/")
CORS(app)

def init_db():
    with sqlite3.connect("todos.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, text TEXT NOT NULL)")

init_db()

@app.route("/todos", methods=["GET"])
def get_todos():
    with sqlite3.connect("todos.db") as conn:
        rows = conn.execute("SELECT id, text FROM todos").fetchall()
        return jsonify([{"id": r[0], "text": r[1]} for r in rows])

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    with sqlite3.connect("todos.db") as conn:
        cur = conn.execute("INSERT INTO todos (text) VALUES (?)", (data["text"],))
        conn.commit()
        return jsonify({"id": cur.lastrowid, "text": data["text"]}), 201

@app.route("/todos/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.get_json()
    with sqlite3.connect("todos.db") as conn:
        conn.execute("UPDATE todos SET text=? WHERE id=?", (data["text"], id))
        conn.commit()
        return jsonify({"id": id, "text": data["text"]})

@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    with sqlite3.connect("todos.db") as conn:
        conn.execute("DELETE FROM todos WHERE id=?", (id,))
        conn.commit()
        return '', 204

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
