import sqlite3

conn = sqlite3.connect("shopsmart.db")
cursor = conn.cursor()

# Products Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    rating REAL,
    category TEXT,
    stock TEXT,
    description TEXT
)
""")

# Orders Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer TEXT,
    product TEXT,
    status TEXT,
    expected_delivery TEXT
)
""")
# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")