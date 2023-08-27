import sqlite3

DATABASE = "user_data.db"

def initialize_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT, leagues TEXT)''')

def add_user(user_id, league):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, leagues) VALUES (?, ?)", (user_id, league))
        conn.commit()

def get_user_leagues(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT leagues FROM users WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()
        if data:
            return data[0].split(',')
        return []

def update_user_leagues(user_id, leagues):
    leagues_str = ','.join(leagues)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET leagues = ? WHERE user_id = ?", (leagues_str, user_id))
        conn.commit()
