from flask import Blueprint, request
from app.utils.decorator_functions import jwt_required_and_not_blacklisted, print_func_name
from app.tasks import service

tasks = Blueprint('webapp', __name__)
@tasks.route("/hello")
@print_func_name
@jwt_required_and_not_blacklisted
def hello():
    return "Hello! "


@tasks.route("/create", methods=['GET', 'POST'])
@print_func_name
@jwt_required_and_not_blacklisted
def create():
    request_body = request.get_json()
    print(request_body)
    return service.create(request_body)


@tasks.route("/list_items/page")
@print_func_name
@jwt_required_and_not_blacklisted
def list_items():
    return service.list_all_items(request)


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


@tasks.route("/update/<item_id>", methods=['PATCH'])
@print_func_name
@jwt_required_and_not_blacklisted
def update_item(item_id):
    request_body = request.get_json()
    return service.update_item(item_id, request_body)


@tasks.route("/upload_attachment/<item_id>", methods=['PUT'])
@print_func_name
@jwt_required_and_not_blacklisted
def upload_attachment(item_id):
    req_files = request.files.get('attachment')
    return service.upload_attachment(item_id, req_files)


@tasks.route("/download_attachment/<item_id>")
@print_func_name
@jwt_required_and_not_blacklisted
def download_attachment(item_id):
    return service.download_attachment(item_id)


@tasks.route("/delete_attachment/<item_id>", methods=['DELETE'])
@print_func_name
@jwt_required_and_not_blacklisted
def delete_attachment(item_id):
    return service.delete_attachment(item_id)


@tasks.route("/similar_tasks/")
@print_func_name
@jwt_required_and_not_blacklisted
def similar_tasks():
    return service.similar_tasks()

