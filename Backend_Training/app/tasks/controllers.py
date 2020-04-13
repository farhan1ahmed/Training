from flask import Blueprint, request
from app.users.service import jwt_required_and_not_blacklisted, print_func_name
from app.tasks import service

tasks = Blueprint('webapp', __name__)
@tasks.route("/hello")
@print_func_name
@jwt_required_and_not_blacklisted
def hello():
    return "Hello World!"


@tasks.route("/create", methods=['GET', 'POST'])
@print_func_name
@jwt_required_and_not_blacklisted
def create():
    request_body = request.get_json()
    print(request_body)
    return service.create(request_body)


@tasks.route("/list_items")
@print_func_name
@jwt_required_and_not_blacklisted
def list_items():
    return service.list_all_items()


@tasks.route("/list_item/<item_id>")
@print_func_name
@jwt_required_and_not_blacklisted
def list_item(item_id):
    return service.list_item(item_id)


@tasks.route("/delete/<item_id>", methods=['DELETE'])
@print_func_name
@jwt_required_and_not_blacklisted
def delete_item(item_id):
    return service.delete_item(item_id)


@tasks.route("/update/<item_id>", methods=['PUT'])
@print_func_name
@jwt_required_and_not_blacklisted
def update_item(item_id):
    request_body = request.get_json()
    return service.update_item(item_id, request_body)


@tasks.route("/upload/<item_id>", methods=['PUT'])
@print_func_name
@jwt_required_and_not_blacklisted
def upload(item_id):
    req_files = request.files.get('attachment')
    return service.upload(item_id, req_files)


@tasks.route("/download/<item_id>")
@print_func_name
@jwt_required_and_not_blacklisted
def download(item_id):
    return service.download(item_id)

