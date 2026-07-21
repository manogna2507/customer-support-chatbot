from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "shopsmart.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            price,
            rating,
            category,
            stock,
            description
        FROM products
    """)

    rows = cursor.fetchall()

    conn.close()

    products = []

    for row in rows:
        products.append({
            "name": row[0],
            "price": row[1],
            "rating": row[2],
            "category": row[3],
            "stock": row[4],
            "description": row[5]
        })

    return products
def create_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )

    conn.commit()
    conn.close()

def get_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user
def check_user(username, password):
    conn = sqlite3.connect("shopsmart.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cursor.fetchone()

    conn.close()

    if row and check_password_hash(row[0], password):
        return True

    return False
import sqlite3

def save_chat(username, user_message, bot_response):
    conn = sqlite3.connect("shopsmart.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history(username, user_message, bot_response)
        VALUES(?,?,?)
        """,
        (username, user_message, bot_response)
    )

    conn.commit()
    conn.close()


def get_chat_history(username):
    conn = sqlite3.connect("shopsmart.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_message, bot_response, timestamp
        FROM chat_history
        WHERE username=?
        ORDER BY id
        """,
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows