from app import db, bcrypt
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from app import login_manager
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



class TodoModel(db.Model):
    __table_args__ = (db.UniqueConstraint('Title', 'userID'),)
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.String, nullable=False, default='Not Started')
    _deleted = db.Column(db.Boolean, default=False)
    CreationDate = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow())
    DueDate = db.Column(db.DateTime, nullable=False)
    CompletionDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    userID = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)


    def __repr__(self):
        return f"""Task('{self.Title}', '{self.Description}', '{self.Status}')"""


