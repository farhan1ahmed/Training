from app import db
from datetime import datetime
from sqlalchemy import event


class TodoModel(db.Model):
    __table_args__ = (db.UniqueConstraint('Title', 'userID'),)
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status_id = db.Column(db.Integer, db.ForeignKey('task_status_options.id'), nullable=False, default=1)
    Status = db.relationship('TaskStatusOptions', primaryjoin='TodoModel.Status_id == TaskStatusOptions.id')
    CreationDate = db.Column(db.DateTime,  nullable=False, default=datetime.utcnow())
    DueDate = db.Column(db.DateTime, nullable=False)
    CompletionDate = db.Column(db.DateTime, nullable=True)
    Attachment_name = db.Column(db.String, nullable=True)
    Attachment_data = db.Column(db.String, nullable=True)
    userID = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

    def __repr__(self):
        return f"""\"Title: {self.Title}, Description: {self.Description}, Status: {self.Status.option}\""""

    @property
    def list_all(self):
        return {
            'id': self.id,
            'Title': self.Title,
            'Description': self.Description,
            'userID': self.userID,
            'Status': self.Status.option,
            'CompletionDate': self.CompletionDate,
            'DueDate': self.DueDate
        }


class TaskStatusOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String, nullable=False)


def initialize_status_table(*args, **kwargs):
    option_1 = TaskStatusOptions(option='Not Started')
    option_2 = TaskStatusOptions(option='Task in progress')
    option_3 = TaskStatusOptions(option='Completed')
    db.session.add(option_1)
    db.session.add(option_2)
    db.session.add(option_3)
    db.session.commit()


event.listen(TaskStatusOptions.__table__, 'after_create', initialize_status_table)




