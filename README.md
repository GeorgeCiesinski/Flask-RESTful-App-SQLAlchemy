# Flask Restful App

This is a Flask Restful API which allows new users to register, authorize which provides a JWT token, and interact 
with Store and Item tables. Available commands are GET, POST, PUT, and DELETE.

# Implementation

1. Clone repository
2. Create a virtual machine, and use pip to install the requirements
```
pip install -r requirements.txt
```
3. cd into app folder, and run app.py
```
cd app
python app.py
```
4. Use Postman to interact with API. 

# Technology

- Flask
- FlaskRESTful
- Flask SQLAlchemy
- SQLite3

# Limitations

Due to the limitations of SQLite 3, it is not possible to write to multiple tables at once, and the ORM is very limited,
allowing items to be created with store id's which may not exist yet. 