from flask import Blueprint, request
from app.users.service import jwt_required_and_not_blacklisted
from .service import ToDoService

tasks = Blueprint('webapp', __name__)
@tasks.route("/hello")
@jwt_required_and_not_blacklisted
def hello():
    return "Hello World!"


@tasks.route("/home")
@jwt_required_and_not_blacklisted
def home():
    return "Home!"


@tasks.route("/create", methods=['GET', 'POST'])
@jwt_required_and_not_blacklisted
def create():
    request_body = request.get_json()
    return ToDoService().create(request_body)


@tasks.route("/list_items")
@jwt_required_and_not_blacklisted
def list_items():
    return ToDoService().list_all_items()


@tasks.route("/list_item/<item_id>")
@jwt_required_and_not_blacklisted
def list_item(item_id):
    return ToDoService().list_item(item_id)


@tasks.route("/delete/<item_id>")
@jwt_required_and_not_blacklisted
def delete_item(item_id):
    return ToDoService().delete_item(item_id)
