from db import db


# Create a superclass of db.Model so SQLAlchemy knows this objects will be saved to a database
class StoreModel(db.Model):

	# Table name
	__tablename__ = 'stores'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	# Relationships
	# lazy turns the relationship from a list of items to a query builder that has the ability to look into the items table
	items = db.relationship('ItemModel', lazy='dynamic')

	def __init__(self, name):
		self.name = name

	def json(self):
		# all() is required to view a relationship with dynamic lazy loading
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
