from flask import Response, jsonify, url_for, request
import datetime
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from .models import UserModel, BlackList
from app import app, db, mail, status_codes
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from functools import wraps


def generate_email_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['PASSWORD_SALT'])


def confirm_email_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['PASSWORD_SALT'] , max_age=expiration)
    except:
        return False
    return email


def send_confirmation_email(email):
    confirm_url = url_for('register.confirm_user', token=generate_email_token(email), _external=True)
    msg = Message(subject='ToDo App: Confirm your Email', body=confirm_url, recipients=[email], sender=app.config['DEFAULT_MAIL_SENDER'])
    mail.send(msg)


def jwt_required_and_not_blacklisted(fn):
    @wraps(fn)
    def wrapper(*arg, **kwargs):
        verify_jwt_in_request()
        token = request.headers.get('Authorization').split(" ")[1]
        token_b_listed = BlackList.query.filter_by(token=token).first()
        if token_b_listed:
            return Response('{"message":"Token expired on logging out. Login again to continue"}', status=status_codes['UNAUTHORIZED'], mimetype='application/json')
        else:
            return fn(*arg, **kwargs)
    return wrapper


class UserService:
    def register_user(self, request_body):
        user = UserModel(username=request_body.get('username'), email=request_body.get('email'), password=request_body.get('password'))
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user.email)
        return Response('{"message":"success"}', status=status_codes['CREATED'], mimetype='application/json')

    def login_user(self, request_body):
        user = UserModel.query.filter_by(email=request_body.get('email')).first()
        print(user)
        credentials_proved = check_password_hash(user.password, request_body.get('password'))

        if not credentials_proved:
            return Response('{"message":"Invalid email or password"}', status=status_codes['UNAUTHORIZED'], mimetype='application/json')
        if not user.confirmed:
            return Response('{"message":"Confirm Email to continue"}', status=status_codes['UNAUTHORIZED'], mimetype='application/json')
        life = datetime.timedelta(days=2)
        access_token = create_access_token(identity=str(user.id), expires_delta=life)
        response = jsonify(message='success', token=access_token)
        response.status_code = status_codes['SUCCESS']
        return response

    def confirm_user(self, token, status):
        try:
            email = confirm_email_token(token)
        except:
            return Response('{"message":"Confirmation link has expired"}', status=status_codes['FORBIDDEN'], mimetype='application/json')
        user = UserModel.query.filter_by(email=email).first()
        if status.get('status') == 'cancel':
            db.session.delete(user)
            db.session.commit()
            return Response('{"message":"User deleted successfully"}', status=status_codes['SUCCESS'], mimetype='application/json')
        elif status.get('status') == 'confirm':
            if user.confirmed:
                return Response('{"message":"User already confirmed"}', status=status_codes['SUCCESS'], mimetype='application/json')
            else:
                user.confirmed = True
                db.session.add(user)
                db.session.commit()
                return Response('{"message":"You have confirmed successfully"}', status=status_codes['SUCCESS'],
                                mimetype='application/json')

    def logout_user(self, token):
        blacklist_this_token = BlackList(token)
        db.session.add(blacklist_this_token)
        db.session.commit()
        return Response('{"message":"Logged Out successfully"}', status=status_codes['SUCCESS'],
                    mimetype='application/json')




