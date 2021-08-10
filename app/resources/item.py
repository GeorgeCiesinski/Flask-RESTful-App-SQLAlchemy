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
	parser.add_argument(
		'store_id',
		type=int,
		required=True,
		help="Every item needs a store_id!"
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

		item = ItemModel(name, data['price'], data['store_id'])

		# Calls the insert function
		try:
			item.save_to_db()
		except Exception as e:
			exception_message = e
			return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error

		return item.json(), 201

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

	@jwt_required()
	def put(self, name):
		# This uses the json payload and only uses the arguments defined in the parser argument
		data = self.parser.parse_args()

		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, **data)  # Unpacks data['price'], data['store_id'] into kwargs
		else:
			item.price = data['price']
			item.store_id = data['store_id']

		item.save_to_db()

		return item.json()


class ItemList(Resource):

	def get(self):
		return {'items': [item.json() for item in ItemModel.query.all()]}
