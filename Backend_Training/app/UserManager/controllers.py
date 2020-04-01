from flask import Blueprint, request, Response, jsonify
from app import db
from .email_confirmation import send_confirmation_email, confirm_email_token
from app.database_structure import UserModel
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
import datetime


UserManager = Blueprint('register', __name__)
@UserManager.route("/register", methods=['POST'])
def register_user():
    user = UserModel(**request.get_json())
    db.session.add(user)
    db.session.commit()
    send_confirmation_email(user.email)
    return Response('{"message":"success"}', status=201, mimetype='application/json')


@UserManager.route("/login", methods=['GET', 'POST'])
def login_user():
    request_body = request.get_json()
    user = UserModel.query.filter_by(email=request_body.get('email')).first()
    print(user)
    credentials_proved = check_password_hash(user.password, request_body.get('password'))

    if not credentials_proved:
        return Response('{"message":"Invalid email or password"}', status=401, mimetype='application/json')
    if not user.confirmed:
        return Response('{"message":"Confirm Email to continue"}', status=401, mimetype='application/json')
    life = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=life)
    response = jsonify(message='success', token=access_token)
    response.status_code = 201
    return response


@UserManager.route("/confirm/<token>", methods=['GET'])
def confirm_user(token):
    status = request.get_json()
    try:
        email = confirm_email_token(token)
    except:
        return Response('{"message":"Confirmation link has expired"}', status=404, mimetype='application/json')
    user = UserModel.query.filter_by(email=email).first()
    if status['status'] == 'cancel':
        db.session.delete(user)
        db.session.commit()
        return Response('{"message":"User deleted successfully"}', status=201, mimetype='application/json')
    elif status['status'] == 'confirm':
        if user.confirmed:
            return Response('{"message":"User already confirmed"}', status=201, mimetype='application/json')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            return Response('{"message":"You have confirmed successfully"}', status=201, mimetype='application/json')

