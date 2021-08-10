from db import db


# Create a superclass of db.Model so SQLAlchemy knows this objects will be saved to a database
class UserModel(db.Model):

	# Table name
	__tablename__ = 'users'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))  # Limits the characters in the string to 80
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		# SQLAlchemy gets the row and converts it into the model object
		return cls.query.filter_by(username=username).first()  # same as SELECT * FROM items WHERE username=username

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()  # same as SELECT * FROM items WHERE id=_id
