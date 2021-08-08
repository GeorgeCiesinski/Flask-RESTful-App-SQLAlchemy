from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy object - Links to Flask app, and looks at all objects. Maps those objects to rows in db.
db = SQLAlchemy()