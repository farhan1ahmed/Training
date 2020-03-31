from itsdangerous import URLSafeTimedSerializer
from app import app, mail
from flask import url_for
from flask_mail import Message
from functools import wraps


def generate_email_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=b'6dfde280ba245')


def confirm_email_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=b'6dfde280ba245', max_age=expiration)
    except:
        return False
    return email


def send_confirmation_email(email):
    confirm_url = url_for('register.confirm_user', token=generate_email_token(email), _external=True)
    msg = Message(subject='ToDo App: Confirm your Email', body=confirm_url, recipients=[email], sender=app.config['DEFAULT_MAIL_SENDER'])
    mail.send(msg)

