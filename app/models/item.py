from db import db


# Create a superclass of db.Model so SQLAlchemy knows this objects will be saved to a database
class ItemModel(db.Model):

	# Table name
	__tablename__ = 'items'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))  # Decimal with precision of two spaces
	# Foreign key linked to primary key of another table
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # Foreign Key prevents that id from being deleted if another table is using that foreign key

	# Relationships
	store = db.relationship('StoreModel')

	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name': self.name, 'price': self.price}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()  # same as SELECT * FROM items WHERE name=name

	# Upserts to database
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
