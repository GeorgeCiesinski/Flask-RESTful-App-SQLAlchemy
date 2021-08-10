from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

# Create flask app
app = Flask(__name__)
# SQLALCHEMY database will live at the root folder of the project
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Can be PostgreSQL
# Stop FlaskSQLAlchemy from tracking changes so we can use the base SQLAlchemy tracker instead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# This should be secret, not hard coded. Using name for learning purposes
app.secret_key = 'george'
# Create an api for flask_restful
api = Api(app)


# Creates the data.db file before the first request is ran.
@app.before_first_request
def create_tables():
	db.create_all()  # Relies on the model being imported for it to see the model/table


jwt = JWT(app, authenticate, identity)

# Add resource to api
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	# Initialize SQLAlchemy object
	db.init_app(app)
	# Start app
	app.run(port=5000, debug=True)
