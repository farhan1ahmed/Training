from flask import Blueprint, request
from .service import UserService, jwt_required_and_not_blacklisted


users = Blueprint('register', __name__)
@users.route("/register", methods=['POST'])
def register_user():
    request_body = request.get_json()
    return UserService().register_user(request_body)


@users.route("/login", methods=['GET', 'POST'])
def login_user():
    request_body = request.get_json()
    return UserService().login_user(request_body)


@users.route("/confirm/<token>", methods=['GET'])
def confirm_user(token):
    status = request.get_json()
    return UserService().confirm_user(token, status)


@users.route("/logout", methods=['GET', 'POST'])
@jwt_required_and_not_blacklisted
def logout_user():
    token = request.headers.get('Authorization').split(" ")[1]
    return UserService().logout_user(token)
