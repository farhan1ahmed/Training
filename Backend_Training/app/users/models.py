from app import db
from flask_bcrypt import generate_password_hash
from datetime import datetime
from sqlalchemy import event


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False, default=1)
    user_type = db.relationship('UserType', primaryjoin='UserModel.user_type_id == UserType.id')
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    tasks = db.relationship('TodoModel', backref='user_model', primaryjoin='UserModel.id == TodoModel.userID')

    def hash_password(self, password):
        return generate_password_hash(password).decode('utf-8')

    def __init__(self, username, email, password):
        self.username = username
        if password is not None:
            self.password = self.hash_password(password)
        self.email = email

    def __repr__(self):
        return f"""User('{self.username}', '{self.email}', '{self.confirmed}', '{self.user_type.type}')"""


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)


def initialize_user_types(*args, **kwargs):
    option_1 = UserType(type='App User')
    option_2 = UserType(type='FB User')
    db.session.add(option_1)
    db.session.add(option_2)
    db.session.commit()


event.listen(UserType.__table__, 'after_create', initialize_user_types)


class BlackList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    black_listed_on = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow())

    def __init__(self, token):
        self.token = token



