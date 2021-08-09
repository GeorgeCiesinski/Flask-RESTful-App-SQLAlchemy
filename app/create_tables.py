import sqlite3

"""
Sets up tables for the first time.
cd into app folder, then the below command in terminal:

python create_tables.py
"""

connection = sqlite3.connect('data.db')  # Database connection
cursor = connection.cursor()  # Interacts with db

# SQL Query: Create users table if doesn't exist
# INTEGER PRIMARY KEY tells the db to auto increment. Normally we can use int for this data type.
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# real is a decimal type in SQL
create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

connection.commit()

connection.close()
