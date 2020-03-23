from flask import jsonify, Blueprint
from app.mod_webapp.helper import ToDoHelper
from flask_login import login_required

mod_webapp = Blueprint('webapp', __name__)
@mod_webapp.route("/hello")
@login_required
def hello():
    return "Hello World!"

@mod_webapp.route("/home")
@login_required
def home():
    return "Home!"


@mod_webapp.route("/todo")
@login_required
def list_todo():
    return jsonify(ToDoHelper.list())