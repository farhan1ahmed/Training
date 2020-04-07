from flask import Response, jsonify
from flask_jwt_extended import get_jwt_identity
import datetime
from .models import TodoModel
from app import db, status_codes


class ToDoService:
    def create(self, request_body):
        duedate = datetime.date(int(request_body.get('DueDate')[0:4]), int(request_body.get('DueDate')[5:7]),
                                int(request_body.get('DueDate')[8:10]))
        task = TodoModel(Title=request_body.get('Title'), Description=request_body.get('Description'), DueDate=duedate,
                         userID=get_jwt_identity())
        db.session.add(task)
        db.session.commit()
        return Response('{"message":"success"}', status=status_codes['CREATED'], mimetype='application/json')

    def list_all_items(self):
        user = get_jwt_identity()
        tasks = TodoModel.query.filter_by(userID=user).all()
        return jsonify([i.list_all for i in tasks])

    def list_item(self, item_id):
        user = get_jwt_identity()
        tasks = TodoModel.query.filter_by(userID=user).filter_by(id=item_id)
        return jsonify([i.list_all for i in tasks])

    def delete_item(self, item_id):
        user = get_jwt_identity()
        task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
        if task is None:
            return Response('{"message":"No such task exists."}', status=status_codes['NOT FOUND'], mimetype='application/json')
        db.session.delete(task)
        db.session.commit()
        return Response('{"message":"Task deleted successfully"}', status=status_codes['SUCCESS'], mimetype='application/json')

    def update_item(self, item_id, request_body):
        user = get_jwt_identity()
        task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
        if task is None:
            return Response('{"message":"No such task exists."}', status=status_codes['NOT FOUND'], mimetype='application/json')
        if request_body.get('Title'):
            task.Title = request_body.get('Title')
        if request_body.get('Description'):
            task.Description = request_body.get('Description')
        if request_body.get('DueDate'):
            duedate = datetime.date(int(request_body.get('DueDate')[0:4]), int(request_body.get('DueDate')[5:7]),
                                    int(request_body.get('DueDate')[8:10]))
            task.DueDate = duedate
        if request_body.get('Status'):
            task.Status = request_body.get('Status')
            if request_body.get('Status') == 'Completed':
                task.CompletionDate = datetime.datetime.utcnow()
        db.session.commit()
        return Response('{"message":"Task updated successfully"}', status=status_codes['SUCCESS'],
                        mimetype='application/json')







