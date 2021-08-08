import sqlite3
from db import db


# Create a superclass of db.Model so SQLAlchemy knows this objects will be saved to a database
class ItemModel(db.Model):

	# Table name
	__tablename__ = 'items'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))  # Decimal with precision of two spaces

	def __init__(self, name, price):
		self.name = name
		self.price = price

	def json(self):
		return {'name': self.name, 'price': self.price}

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))  # Value must be a tuple, even if it is a single item
		row = result.fetchone()

		connection.close()

		if row:
			# Return instance of ItemModel
			return cls(*row)  # Unpacks row[0], and row[1] into the parameters of __init__()

	def insert(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(query, (self.name, self.price))

		connection.commit()
		connection.close()

	def update(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET price=? WHERE name=?"  # Updates column of item where name matches
		cursor.execute(query, (self.price, self.name))

		connection.commit()
		connection.close()
