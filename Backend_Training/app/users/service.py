"""
    Functions to handle user related requests.

    A module that contains the business logic to implement and handle the
    user related API requests. Each function either sends back a Response object
    to the client corresponding to their query, returns a identity-encoded token
    or sends an email to the user.

    Typical usage example:
    return service.register_user(request_body)
    return service.confirm_user(token, status)
    send_password_reset_email(email)

"""

from flask import Response, url_for
import datetime
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from .models import UserModel, BlackList
from app import app, db, mail
from app.utils import status_codes
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message


SECRET_KEY = 'SECRET_KEY'
PASSWORD_SALT = 'PASSWORD_SALT'
DEFAULT_MAIL_SENDER = 'DEFAULT_MAIL_SENDER'
EMAIL_LINK_EXPIRY = 3600  # seconds
USERNAME = 'username'
PASSWORD = 'password'
EMAIL = 'email'
STATUS_CANCEL = 'cancel'
STATUS_CONFIRM = 'confirm'


# Functions related to Confirmation Email Handling
def generate_email_token(email):
    """ Generates a unique token that can be used to create URLs.

    Encodes the email of the user in a token. The encoding combination uses
    SECRET_KEY and a PASSWORD_SALT.

    Args:
        email: The email id of the user.

    Returns:
        A token string which has the email identity encoded in it. For example:

        "ImZhcmhhbjFha....zYnFyn5qEKuRR5ESK2_Gs3Lx8M"
    """
    serializer = URLSafeTimedSerializer(app.config.get(SECRET_KEY))
    return serializer.dumps(email, salt=app.config.get(PASSWORD_SALT))


def send_confirmation_email(email):
    confirm_url = url_for('user.confirm_user', token=generate_email_token(email), _external=True)
    msg = Message(subject='ToDo App: Confirm your Email', body=confirm_url, recipients=[email], sender=DEFAULT_MAIL_SENDER)
    mail.send(msg)


# User Registration/ Login / Confirm Email/ Logout
def register_user(request_body):
    user = UserModel(username=request_body.get(USERNAME), email=request_body.get(EMAIL), password=request_body.get(PASSWORD))
    db.session.add(user)
    db.session.commit()
    send_confirmation_email(user.email)
    return Response('{"message":"success"}', status=status_codes.CREATED, mimetype='application/json')


def login_user(request_body):
    user = UserModel.query.filter_by(email=request_body.get(EMAIL)).first()
    print(user)
    credentials_proved = check_password_hash(user.password, request_body.get(PASSWORD))

    if not credentials_proved:
        return Response('{"message":"Invalid email or password"}', status=status_codes.UNAUTHORIZED,
                        mimetype='application/json')
    if not user.confirmed:
        return Response('{"message":"Confirm Email to continue"}', status=status_codes.UNAUTHORIZED,
                        mimetype='application/json')
    life = datetime.timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=life)
    res = Response('{"message": "Success"}', status=status_codes.OK, mimetype='application/json')
    #set_access_cookies(res, access_token)
    res.set_cookie("access_token_cookie", value=access_token)
    res.set_cookie("csrf_access_token", value=app.config.get(SECRET_KEY))
    return res


def confirm_user(token, status):
    serializer = URLSafeTimedSerializer(app.config.get(SECRET_KEY))
    email = serializer.loads(token, salt=app.config.get(PASSWORD_SALT), max_age=EMAIL_LINK_EXPIRY)
    user = UserModel.query.filter_by(email=email).first()
    if status == STATUS_CANCEL:
        db.session.delete(user)
        db.session.commit()
        return Response('{"message":"User deleted successfully"}', status=status_codes.NOT_FOUND,
                        mimetype='application/json')
    elif status == STATUS_CONFIRM:
        if user.confirmed:
            return Response('{"message":"User already confirmed"}', status=status_codes.OK,
                            mimetype='application/json')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            return Response('{"message":"You have confirmed successfully"}', status=status_codes.OK,
                            mimetype='application/json')


def logout_user(token):
    blacklist_this_token = BlackList(token)
    db.session.add(blacklist_this_token)
    db.session.commit()
    res = Response('{"message":"Logged Out successfully"}', status=status_codes.OK,
                   mimetype='application/json')
    res.delete_cookie('access_token_cookie')
    res.delete_cookie('csrf_access_token')
    return res


def send_password_reset_email(email):
    reset_url = url_for('user.reset_password', resettoken=generate_email_token(email), _external=True)
    msg = Message(subject='ToDo App: Password Reset', body=reset_url, recipients=[email],
                  sender=DEFAULT_MAIL_SENDER)
    mail.send(msg)


def forgot_password(request_body):
    user_email = request_body.get(EMAIL)
    user = UserModel.query.filter_by(email=user_email).first()
    if not user:
        return Response('{"message":"No such Email registered in database"}', status=status_codes.NOT_FOUND,
                        mimetype='application/json')
    send_password_reset_email(user.email)
    return Response('{"message":"success"}', status=status_codes.OK, mimetype='application/json')


def reset_password(request_body, reset_token):
    serializer = URLSafeTimedSerializer(app.config.get(SECRET_KEY))
    user_email = serializer.loads(reset_token, salt=app.config.get(PASSWORD_SALT), max_age=EMAIL_LINK_EXPIRY)
    if request_body is None:
        return Response('{"message":"New password not provided"}', status=status_codes.FORBIDDEN,
                        mimetype='application/json')
    new_password = request_body.get(PASSWORD)
    user = UserModel.query.filter_by(email=user_email).first()
    if not user:
        return Response('{"message":"No such user registered in database"}', status=status_codes.NOT_FOUND,
                        mimetype='application/json')
    user.password = user.hash_password(new_password)
    db.session.commit()
    return Response('{"message":"Password changed successfully"}', status=status_codes.OK, mimetype='application/json')
