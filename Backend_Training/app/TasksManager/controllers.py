from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.database_structure import TodoModel
import datetime

TasksManager = Blueprint('webapp', __name__)
@TasksManager.route("/hello")
@jwt_required
def hello():
    return "Hello World!"

@TasksManager.route("/home")
@jwt_required
def home():
    return "Home!"


@TasksManager.route("/create", methods=['GET', 'POST'])
@jwt_required
def create():
    request_body = request.get_json()
    duedate = datetime.date(int(request_body.get('DueDate')[0:4]), int(request_body.get('DueDate')[5:7]), int(request_body.get('DueDate')[9:11]))
    print(duedate)
    task = TodoModel(Title=request_body.get('Title'), Description=request_body.get('Description'), DueDate=duedate , userID=get_jwt_identity())
    db.session.add(task)
    db.session.commit()
    return Response('{"message":"success"}', status=201, mimetype='application/json')

@TasksManager.route("/list_items")
@jwt_required
def list_items():
    user = get_jwt_identity()
    tasks = TodoModel.query.filter_by(userID=user).all()
    return jsonify([i.list_all for i in tasks])

@TasksManager.route("/list_item/<item_id>")
@jwt_required
def list_item(item_id):
    user = get_jwt_identity()
    tasks = TodoModel.query.filter_by(userID=user).filter_by(id=item_id)
    return jsonify([i.list_all for i in tasks])

@TasksManager.route("/delete/<item_id>")
@jwt_required
def delete_item(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No such task exists."}', status=404, mimetype='application/json')
    db.session.delete(task)
    db.session.commit()
    return Response('{"message":"Task deleted successfully"}', status=201, mimetype='application/json')