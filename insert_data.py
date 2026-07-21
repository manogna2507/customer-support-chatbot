import sqlite3
import json

# Connect to database
conn = sqlite3.connect("shopsmart.db")
cursor = conn.cursor()

# Load products from JSON
with open("data/products.json", "r") as file:
    products = json.load(file)

# Clear existing data (avoids duplicates)
cursor.execute("DELETE FROM products")

# Insert products
for product in products:
    cursor.execute("""
        INSERT INTO products
        (name, price, rating, category, stock, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product["name"],
        product["price"],
        product["rating"],
        product["category"],
        product["stock"],
        product["description"]
    ))

conn.commit()
conn.close()

print("✅ Products inserted successfully!")