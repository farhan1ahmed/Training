from app import db
from datetime import datetime


class TodoModel(db.Model):
    __table_args__ = (db.UniqueConstraint('Title', 'userID'),)
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.String, nullable=False, default='Not Started')
    CreationDate = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow())
    DueDate = db.Column(db.DateTime, nullable=False)
    CompletionDate = db.Column(db.DateTime, nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)


    def __repr__(self):
        return f"""Task('{self.Title}', '{self.Description}', '{self.Status}')"""

    @property
    def list_all(self):
        return {
            'id': self.id,
            'Title': self.Title,
            'Description': self.Description,
            'userID': self.userID,
            'Status': self.Status,
            'CompletionDate': self.CompletionDate,
            'DueDate': self.DueDate
        }
