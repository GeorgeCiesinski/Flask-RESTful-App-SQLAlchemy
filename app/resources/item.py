import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Api works with resources, every resource has to be a class
class Item(Resource):

	# Parser object to parse request
	parser = reqparse.RequestParser()
	# Parser definition
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help="This field cannot be left blank!"
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)

		if item:
			return item.json()
		return {'message': 'Item not found'}, 404

	def post(self, name):
		data = self.parser.parse_args()

		if ItemModel.find_by_name(name):
			return {'message': f'An item with name {name} already exists.'}, 400

		item = ItemModel(name, data['price'])

		# Calls the insert function
		try:
			item.insert()
		except Exception as e:
			exception_message = e
			return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error

		return item.json(), 201

	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()

		return {'message': 'Item deleted'}

	@jwt_required()
	def put(self, name):
		# This uses the json payload and only uses the arguments defined in the parser argument
		data = self.parser.parse_args()

		item = ItemModel.find_by_name(name)

		updated_item = ItemModel(name, data['price'])

		if item is None:
			try:
				updated_item.insert()
			except Exception:
				return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error
		else:
			try:
				updated_item.update()
			except Exception:
				return {'message': 'An error occurred updating the item.'}, 500  # Internal server error

		return updated_item.json()


class ItemList(Resource):

	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items"  # Updates column of item where name matches
		result = cursor.execute(query)

		items = []

		for row in result:
			items.append({'name': row[0], 'price': row[1]})

		connection.close()

		return {'items': items}
