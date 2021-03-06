from flask import Blueprint, request
from app.utils.decorator_functions import jwt_required_and_not_blacklisted, print_func_name
from app.tasks import service

tasks = Blueprint('webapp', __name__)
@tasks.route("/hello")
@print_func_name
@jwt_required_and_not_blacklisted
def hello():
    return "Hello! "


@tasks.route("/create", methods=['POST'])
@print_func_name
@jwt_required_and_not_blacklisted
def create_task():
    request_body = request.get_json()
    return service.create_task(request_body)


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


@tasks.route("/similar_tasks")
@print_func_name
@jwt_required_and_not_blacklisted
def similar_tasks():
    return service.similar_tasks()


@tasks.route("/reports/tasks_opened_week")
@print_func_name
@jwt_required_and_not_blacklisted
def tasks_opened_week():
    return service.tasks_opened_week()


@tasks.route("/reports/max_tasks_day")
@print_func_name
@jwt_required_and_not_blacklisted
def max_tasks_day():
    return service.max_tasks_day()


@tasks.route("/reports/late_tasks")
@print_func_name
@jwt_required_and_not_blacklisted
def late_tasks():
    return service.late_tasks()


@tasks.route("/reports/avg_tasks_per_day")
@print_func_name
@jwt_required_and_not_blacklisted
def avg_tasks_per_day():
    return service.avg_tasks_per_day()


@tasks.route("/reports/tasks_count_breakdown")
@print_func_name
@jwt_required_and_not_blacklisted
def tasks_count_breakdown():
    return service.tasks_count_breakdown()
