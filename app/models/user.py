import sqlite3
from db import db


# Create a superclass of db.Model so SQLAlchemy knows this objects will be saved to a database
class UserModel(db.Model):

	# Table name
	__tablename__ = 'users'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))  # Limits the characters in the string to 80
	password = db.Column(db.String(80))

	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username=?"
		# To execute queries, execute requires a tuple. Single item tuple must have comma.
		result = cursor.execute(query, (username,))

		# Get first row out of result set
		row = result.fetchone()
		if row:
			# Pass row[0], row[1], row [2]. * extracts ordered fields.
			user = cls(*row)
		else:
			user = None

		# Close connection once done
		connection.close()

		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id=?"
		# To execute queries, execute requires a tuple. Single item tuple must have comma.
		result = cursor.execute(query, (_id,))

		# Get first row out of result set
		row = result.fetchone()
		if row:
			# Pass row[0], row[1], row [2]. * extracts ordered fields.
			user = cls(*row)
		else:
			user = None

		# Close connection once done
		connection.close()

		return user
