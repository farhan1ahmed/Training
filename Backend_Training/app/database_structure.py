from app import db
from flask_login import UserMixin
from app import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, unique=True, nullable=False)
    Email = db.Column(db.String, unique=True, nullable=False)
    Password = db.Column(db.String, unique=True, nullable=False)
    tasks = db.relationship('TodoModel', backref='user', primaryjoin='UserModel.id == TodoModel.userID')

    def __repr__(self):
        return f"""User('{self.username}', '{self.email}')"""


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, unique=True, nullable=False)
    Description = db.Column(db.Text, unique=True, nullable=False)
    Status = db.Column(db.String, unique=True, nullable=False, default='Not Started')
    _deleted = db.Column(db.Boolean, default=False)
    CreationDate = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow())
    DueDate = db.Column(db.DateTime, nullable=False)
    CompletionDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    userID = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

    def __repr__(self):
        return f"""User('{self.Title}', '{self.Description}', '{self.Status}')"""


