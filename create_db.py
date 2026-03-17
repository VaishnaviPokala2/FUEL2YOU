import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
role TEXT
)
""")

# Fuel price table
cur.execute("""
CREATE TABLE IF NOT EXISTS fuel_price(
id INTEGER PRIMARY KEY AUTOINCREMENT,
fuel TEXT,
price REAL
)
""")

# Orders table
cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
fuel TEXT,
quantity REAL,
total REAL,
address TEXT,
payment TEXT,
status TEXT
)
""")

# Default fuel prices
cur.execute("INSERT INTO fuel_price (fuel,price) VALUES ('Petrol',105)")
cur.execute("INSERT INTO fuel_price (fuel,price) VALUES ('Diesel',95)")

# Admin account
cur.execute("INSERT INTO users VALUES (NULL,'Admin','admin@gmail.com','admin123','admin')")

# Delivery agent account
cur.execute("INSERT INTO users VALUES (NULL,'Agent','agent@gmail.com','agent123','agent')")

conn.commit()
conn.close()

print("Database Created Successfully")