from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.database_structure import TodoModel
import datetime

mod_webapp = Blueprint('webapp', __name__)
@mod_webapp.route("/hello")
@jwt_required
def hello():
    return "Hello World!"

@mod_webapp.route("/home")
@jwt_required
def home():
    return "Home!"


@mod_webapp.route("/create", methods=['GET', 'POST'])
@jwt_required
def create():
    request_body = request.get_json()
    duedate = datetime.date(int(request_body.get('DueDate')[0:4]), int(request_body.get('DueDate')[5:7]), int(request_body.get('DueDate')[9:11]))
    print(duedate)
    task = TodoModel(Title=request_body.get('Title'), Description=request_body.get('Description'), DueDate=duedate , userID=get_jwt_identity())
    db.session.add(task)
    db.session.commit()
    return Response('{"message":"success"}', status=201, mimetype='application/json')