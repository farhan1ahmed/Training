from flask import Response, url_for, request
import datetime
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, verify_jwt_in_request, set_access_cookies
from .models import UserModel, BlackList
from app import app, db, mail, utils
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from functools import wraps

secret_key = 'SECRET_KEY'
password_salt = 'PASSWORD_SALT'
default_mail_sender = 'DEFAULT_MAIL_SENDER'
email_link_expiry = 3600  #seconds
user_name = 'username'
pass_word = 'password'
email = 'email'
status_cancel = 'cancel'
status_confirm = 'confirm'

# Functions related to Confirmation Email Handling
def generate_email_token(email):
    serializer = URLSafeTimedSerializer(app.config.get(secret_key))
    return serializer.dumps(email, salt=app.config.get(password_salt))


def send_confirmation_email(email):
    confirm_url = url_for('user.confirm_user', token=generate_email_token(email), _external=True)
    msg = Message(subject='ToDo App: Confirm your Email', body=confirm_url, recipients=[email], sender=default_mail_sender)
    mail.send(msg)

#Decorator Function to verify JWT token and BlackList Table
def jwt_required_and_not_blacklisted(fn):
    @wraps(fn)
    def wrapper(*arg, **kwargs):
        verify_jwt_in_request()
        token = request.headers.get('Authorization').split(" ")[1]
        token_b_listed = BlackList.query.filter_by(token=token).first()
        if token_b_listed:
            return Response('{"message":"Token expired on logging out. Login again to continue"}', status=utils.UNAUTHORIZED, mimetype='application/json')
        else:
            return fn(*arg, **kwargs)
    return wrapper

def print_func_name(fn):
    @wraps(fn)
    def printer(*args, **kwargs):
        print(fn.__name__)
        return fn(*args, **kwargs)
    return printer


# User Registration/ Login / Confirm Email/ Logout
def register_user(request_body):
    user = UserModel(username=request_body.get(user_name), email=request_body.get(email), password=request_body.get(pass_word))
    db.session.add(user)
    db.session.commit()
    send_confirmation_email(user.email)
    return Response('{"message":"success"}', status=utils.CREATED, mimetype='application/json')

def login_user(request_body):
    user = UserModel.query.filter_by(email=request_body.get(email)).first()
    print(user)
    credentials_proved = check_password_hash(user.password, request_body.get(pass_word))

    if not credentials_proved:
        return Response('{"message":"Invalid email or password"}', status=utils.UNAUTHORIZED, mimetype='application/json')
    if not user.confirmed:
        return Response('{"message":"Confirm Email to continue"}', status=utils.UNAUTHORIZED, mimetype='application/json')
    life = datetime.timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=life)
    res = Response('{"message": "Success"}', status=utils.OK, mimetype='application/json')
    #set_access_cookies(res, access_token)
    res.set_cookie("access_token_cookie", value=access_token)
    res.set_cookie("csrf_access_token", value=app.config.get(secret_key))
    return res

def confirm_user(token, status):
    serializer = URLSafeTimedSerializer(app.config.get(secret_key))
    try:
        email = serializer.loads(token, salt=app.config.get(password_salt), max_age=email_link_expiry)
    except Exception as e:
        print(e)
        return Response(f'{{"message": "{e}"}}', status=utils.SERVER_ERROR, mimetype='application/json')
    user = UserModel.query.filter_by(email=email).first()
    if status == status_cancel:
        db.session.delete(user)
        db.session.commit()
        return Response('{"message":"User deleted successfully"}', status=utils.NOT_FOUND, mimetype='application/json')
    elif status == status_confirm:
        if user.confirmed:
            return Response('{"message":"User already confirmed"}', status=utils.OK, mimetype='application/json')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            return Response('{"message":"You have confirmed successfully"}', status=utils.OK,
                            mimetype='application/json')

def logout_user(token):
    blacklist_this_token = BlackList(token)
    db.session.add(blacklist_this_token)
    db.session.commit()
    res = Response('{"message":"Logged Out successfully"}', status=utils.OK,
                   mimetype='application/json')
    res.delete_cookie('access_token_cookie')
    res.delete_cookie('csrf_access_token')
    return res




