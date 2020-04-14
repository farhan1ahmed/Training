from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask import request, Response
from app.users.models import BlackList
from app.utils import status_codes


def print_func_name(fn):
    @wraps(fn)
    def printer(*args, **kwargs):
        print(fn.__name__)
        return fn(*args, **kwargs)
    return printer


#Decorator Function to verify JWT token and BlackList Table
def jwt_required_and_not_blacklisted(fn):
    @wraps(fn)
    def wrapper(*arg, **kwargs):
        verify_jwt_in_request()
        token = request.headers.get('Authorization').split(" ")[1]
        token_b_listed = BlackList.query.filter_by(token=token).first()
        if token_b_listed:
            return Response('{"message":"Token expired on logging out. Login again to continue"}', status=status_codes.UNAUTHORIZED, mimetype='application/json')
        else:
            return fn(*arg, **kwargs)
    return wrapper