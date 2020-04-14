from flask import Blueprint, request
from app.users import service
from app.utils.decorator_functions import jwt_required_and_not_blacklisted, print_func_name


users = Blueprint('user', __name__)
@users.route("/register", methods=['POST'])
@print_func_name
def register_user():
    request_body = request.get_json()
    return service.register_user(request_body)


@users.route("/login", methods=['GET', 'POST'])
@print_func_name
def login_user():
    request_body = request.get_json()
    return service.login_user(request_body)


@users.route("/confirm/<token>", methods=['GET'])
@print_func_name
def confirm_user(token):
    status = request.args.get('status')
    return service.confirm_user(token, status)


@users.route("/logout", methods=['GET', 'POST'])
@print_func_name
@jwt_required_and_not_blacklisted
def logout_user():
    token = request.headers.get('Authorization').split(" ")[1]
    return service.logout_user(token)
