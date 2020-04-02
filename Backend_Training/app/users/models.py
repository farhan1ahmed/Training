from app import db
from flask_bcrypt import generate_password_hash
from datetime import datetime


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    tasks = db.relationship('TodoModel', backref='user', primaryjoin='UserModel.id == TodoModel.userID')

    def __init__(self, username, email, password):
        self.username = username
        self.password = generate_password_hash(password).decode('utf-8')
        self.email = email

    def __repr__(self):
        return f"""User('{self.username}', '{self.email}', '{self.confirmed}')"""


class BlackList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    black_listed_on = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow())

    def __init__(self, token):
        self.token = token



