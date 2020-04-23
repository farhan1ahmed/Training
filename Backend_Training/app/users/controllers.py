from flask import Blueprint, request, render_template
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


@users.route("/login/facebook", methods=['GET', 'POST'])
@print_func_name
def login_user_fb():
    return render_template('index.html')


@users.route("/API_facebook_login", methods=['POST'])
@print_func_name
def response_from_fb():
    request_body = request.get_json()
    return service.API_facebook_login(request_body)


@users.route("/confirm/<token>", methods=['GET'])
@print_func_name
def confirm_user(token):
    status = request.args.get('status')
    return service.confirm_user(token, status)


@users.route("/logout", methods=['GET', 'POST'])
@print_func_name
@jwt_required_and_not_blacklisted
def logout_user():
    cookie = request.headers.get('Cookie')
    token = cookie.split(sep='access_token_cookie=')[1].split(';')[0]
    return service.logout_user(token)


@users.route("/forgot_password", methods={'GET', 'POST'})
@print_func_name
def forgot_password():
    request_body = request.get_json()
    return service.forgot_password(request_body)


@users.route("/reset_password/<resettoken>", methods={'GET', 'POST'})
@print_func_name
def reset_password(resettoken):
    reset_token = resettoken
    request_body = request.get_json()
    return service.reset_password(request_body, reset_token)