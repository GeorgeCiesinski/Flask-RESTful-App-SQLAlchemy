import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

	parser = reqparse.RequestParser()  # Parser object

	# Username Parser
	parser.add_argument(
		'username',
		type=str,
		required=True,
		help="This field cannot be left blank!"
	)

	# Password parser
	parser.add_argument(
		'password',
		type=str,
		required=True,
		help="This field cannot be left blank!"
	)

	def post(self):
		"""
		Registers a new user and posts the new User object to the database.

		:return: message, http status
		"""

		# Parse json
		data = UserRegister.parser.parse_args()

		# Checks if user already exists
		if UserModel.find_by_username(data['username']):
			return {"message": "A user with that username already exists"}, 400

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		# Query to insert users. First value is NULL because of autoincrement.
		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {"message": "User created successfully."}, 201
