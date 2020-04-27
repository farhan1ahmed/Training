from app.users.models import UserModel
from app.tasks.models import TodoModel
from flask_mail import Message
import sqlalchemy
from app import app
from app import mail
import datetime

COMPLETED = 'completed'


def mail_reminder():
    user_ids = UserModel.query.with_entities(UserModel.id, UserModel.email).all()
    for user in user_ids:
        user_id = list(user)[0]
        email = list(user)[1]
        search_date = f"{datetime.datetime.utcnow().date()}%"
        tasks = TodoModel.query.filter_by(userID=user_id).filter(TodoModel.DueDate.like(search_date)).\
            filter(sqlalchemy.not_(TodoModel.Status.like(COMPLETED))).all()
        if tasks is not None:
            msg_body = "These tasks are due today!\n"
            for task in tasks:
                msg_body = msg_body + f"{task}\n"
            msg = Message(subject='Reminder: Tasks Deadline!', body=msg_body, recipients=[email],
                          sender=app.config.get('DEFAULT_MAIL_SENDER'))
            with app.app_context():
                mail.send(msg)


