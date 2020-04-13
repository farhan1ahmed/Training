from flask import Response, jsonify, send_file
from flask_jwt_extended import get_jwt_identity
import datetime
from .models import TodoModel
from app import db, utils
from io import BytesIO

title = 'Title'
description = 'Description'
duedate = 'DueDate'
status = 'Status'
status_1 = 'Work in Progress'.lower()   #The status of the ongoing task that can be updated by the user
status_2 = 'Completed'.lower()


def create(request_body):
    due_date = datetime.date(int(request_body.get(duedate)[0:4]), int(request_body.get(duedate)[5:7]),
                             int(request_body.get(duedate)[8:10]))
    task = TodoModel(Title=request_body.get(title), Description=request_body.get(description), DueDate=due_date,
                     userID=get_jwt_identity())
    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        print(e)
        return Response(f'{{"message": "{e}"}}', status=utils.FORBIDDEN, mimetype='application/json')
    return Response('{"message":"success"}', status=utils.CREATED, mimetype='application/json')


def list_all_items():
    user = get_jwt_identity()
    tasks = TodoModel.query.filter_by(userID=user).all()
    if tasks is None:
        return Response('{"message":"No Content"}', status=utils.NOT_FOUND, mimetype='application/json')
    return jsonify([i.list_all for i in tasks])


def list_item(item_id):
    user = get_jwt_identity()
    tasks = TodoModel.query.filter_by(userID=user).filter_by(id=item_id)
    if tasks is None:
        return Response('{"message":"No Content"}', status=utils.NOT_FOUND, mimetype='application/json')
    return jsonify([i.list_all for i in tasks])


def delete_item(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No such task exists."}', status=utils.NOT_FOUND, mimetype='application/json')
    db.session.delete(task)
    db.session.commit()
    return Response('{"message":"Task deleted successfully"}', status=utils.OK, mimetype='application/json')


def update_item(item_id, request_body):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No such task exists."}', status=utils.NOT_FOUND, mimetype='application/json')
    if request_body.get(title):
        task.Title = request_body.get(title)
    if request_body.get(description):
        task.Description = request_body.get(description)
    if request_body.get(duedate):
        due_date = datetime.date(int(request_body.get(duedate)[0:4]), int(request_body.get(duedate)[5:7]),
                                 int(request_body.get(duedate)[8:10]))
        task.DueDate = due_date
    if request_body.get(status):
        if request_body.get(status).lower() == status_1:
            task.Status = request_body.get(status)
        elif request_body.get(status).lower() == status_2:
            task.Status = request_body.get(status)
            task.CompletionDate = datetime.datetime.utcnow()
        else:
            return Response('{"message":"Status can be changed either to "Work in Progress" or "Completed" only"}',
                            status=utils.FORBIDDEN, mimetype='application/json')
    db.session.commit()
    return Response('{"message":"Task updated successfully"}', status=utils.OK,
                    mimetype='application/json')


def upload(item_id, req_files):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No Content"}', status=utils.NOT_FOUND, mimetype='application/json')
    task.Attachment_name = req_files.filename
    task.Attachment_data = req_files.read()
    db.session.commit()
    return Response('{"message":"File uploaded successfully"}', status=utils.OK, mimetype='application/json')


def download(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No Content"}', status=utils.NOT_FOUND, mimetype='application/json')
    if task.Attachment_data is None and task.Attachment_name is None:
        return Response('{"message":"No Content"}', status=utils.NOT_FOUND, mimetype='application/json')
    print(task.Attachment_name)
    return send_file(BytesIO(task.Attachment_data), attachment_filename=task.Attachment_name, as_attachment=True)
    #Response('{"message":"File downloaded successfully"}', status=utils.OK, mimetype='application/json')

