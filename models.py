import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # הפעלת תמיכה ב־foreign keys (חובה!)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # יצירת טבלת users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    # יצירת טבלת shifts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shifts (
        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL
    );
    """)

    # יצירת טבלת constraints
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS constraints (
        user_id INTEGER,
        shift_id INTEGER,
        available_key INTEGER DEFAULT 1,
        PRIMARY KEY (user_id, shift_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (shift_id) REFERENCES shifts(shift_id) ON DELETE CASCADE
    );
    """)

    # יצירת טבלת result
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS result (
        shift_id INTEGER,
        user_id INTEGER,
        PRIMARY KEY (shift_id, user_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (shift_id) REFERENCES shifts(shift_id)
    );
    """)

    # טריגר: כאשר מוסיפים shift → יצירת constraints לכל המשתמשים
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS after_insert_shift
    AFTER INSERT ON shifts
    BEGIN
        INSERT INTO constraints (user_id, shift_id, available_key)
        SELECT user_id, NEW.shift_id, 1 FROM users;
    END;
    """)

    # טריגר: כאשר מוסיפים user → יצירת constraints לכל המשמרות
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS after_insert_user
    AFTER INSERT ON users
    BEGIN
        INSERT INTO constraints (user_id, shift_id, available_key)
        SELECT NEW.user_id, shift_id, 1 FROM shifts;
    END;
    """)

    # SQLite כבר תומך במחיקה cascading בזכות ON DELETE CASCADE

    conn.commit()
    conn.close()

init_db()