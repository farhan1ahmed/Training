from flask import Response, json
from flask_jwt_extended import get_jwt_identity
import datetime, os
from .models import TodoModel
from app import db
from app.utils import status_codes
from sqlalchemy import exc

TITLE = 'Title'
DESCRIPTION = 'Description'
DUE_DATE = 'DueDate'
STATUS = 'Status'
STATUS_1 = 'Work in Progress'.lower()   # The status of the ongoing task that can be updated by the user
STATUS_2 = 'Completed'.lower()


def create(request_body):
    """ Creates a task with a unique title and stores it in to the database.

        The task is created as per the attributes defined by the user. The title
        of the tasks for each user must be unique. The task is marked 'Not Started'
        by default.

        Args:
            request_body: The request sent in by the client, containing all the information
                          related to the task.

        Returns:
            A Response object indicating whether the action was successful or not. For example:

            Response('{"message":"success"}', status=status_codes.CREATED, mimetype='application/json')

        Raises:
            IntegrityError: If the Title of the task is not unique, the database refuses to add the new task.
    """
    due_date = datetime.date(int(request_body.get(DUE_DATE)[0:4]), int(request_body.get(DUE_DATE)[5:7]),
                             int(request_body.get(DUE_DATE)[8:10]))
    task = TodoModel(Title=request_body.get(TITLE), Description=request_body.get(DESCRIPTION), DueDate=due_date,
                     userID=get_jwt_identity())
    try:
        db.session.add(task)
        db.session.commit()
    except exc.IntegrityError:
        return Response('{"message": "A task with the same Title occurs already!"}', status=status_codes.FORBIDDEN, mimetype='application/json')
    return Response('{"message":"success"}', status=status_codes.CREATED, mimetype='application/json')


def list_all_items():
    user = get_jwt_identity()
    tasks = TodoModel.query.filter_by(userID=user).all()
    print(tasks)
    if tasks is None:
        return Response('{"message":"No Content"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    return Response(json.dumps([i.list_all for i in tasks]), status=status_codes.NOT_FOUND, mimetype='application/json')


def list_item(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No Content"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    return Response(json.dumps(task.list_all), status=status_codes.NOT_FOUND, mimetype='application/json')


def delete_item(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No such task exists."}', status=status_codes.NOT_FOUND, mimetype='application/json')
    db.session.delete(task)
    db.session.commit()
    return Response('{"message":"Task deleted successfully"}', status=status_codes.OK, mimetype='application/json')


def update_item(item_id, request_body):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No such task exists."}', status=status_codes.NOT_FOUND, mimetype='application/json')
    if request_body.get(TITLE):
        task.Title = request_body.get(TITLE)
    if request_body.get(DESCRIPTION):
        task.Description = request_body.get(DESCRIPTION)
    if request_body.get(DUE_DATE):
        due_date = datetime.date(int(request_body.get(DUE_DATE)[0:4]), int(request_body.get(DUE_DATE)[5:7]),
                                 int(request_body.get(DUE_DATE)[8:10]))
        task.DueDate = due_date
    if request_body.get(STATUS):
        if request_body.get(STATUS).lower() == STATUS_1:
            task.Status = request_body.get(STATUS)
        elif request_body.get(STATUS).lower() == STATUS_2:
            task.Status = request_body.get(STATUS)
            task.CompletionDate = datetime.datetime.utcnow()
        else:
            return Response('{"message":"Status can be changed either to "Work in Progress" or "Completed" only"}',
                            status=status_codes.FORBIDDEN, mimetype='application/json')
    try:
        db.session.commit()
    except exc.IntegrityError:
        return Response('{"message": "A task with the same Title occurs already!"}', status=status_codes.FORBIDDEN,
                        mimetype='application/json')
    return Response('{"message":"Task updated successfully"}', status=status_codes.OK,
                    mimetype='application/json')


def upload_attachment(item_id, req_files):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No Content"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    task.Attachment_name = req_files.filename
    # In order to differentiate between files with the same name, but belonging to different users
    # the user.id is prepended with the file name. This way a file with "some_name" will be stored
    # as "1_some_name", "2_some_name", "3_some_name" and so on.
    save_path = os.path.join(os.environ.get('UPLOAD_FOLDER'), user + "_" + req_files.filename)
    with open(save_path, 'wb') as f:
        data = req_files.read()
        f.write(data)
        f.close()
    task.Attachment_data = os.path.abspath(save_path)
    db.session.commit()
    return Response('{"message":"File uploaded successfully"}', status=status_codes.OK, mimetype='application/json')


def download_attachment(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No Content"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    if task.Attachment_data is None and task.Attachment_name is None:
        return Response('{"message":"No Content"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    with open(task.Attachment_data, 'rb') as f:
        download_file = f.read()
        f.close()
    return Response(download_file, status=status_codes.OK,
                    headers={'Content-disposition': 'attachment; filename=\"' + task.Attachment_name + '\"'})


def delete_attachment(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No such task exists."}', status=status_codes.NOT_FOUND,
                        mimetype='application/json')
    if task.Attachment_name is None and task.Attachment_data is None:
        return Response('{"message":"There is no attachment with this item"}', status=status_codes.NOT_FOUND,
                        mimetype='application/json')
    os.unlink(task.Attachment_data)
    task.Attachment_name = None
    task.Attachment_data = None
    db.session.commit()
    return Response('{"message":"Attachment deleted successfully"}', status=status_codes.OK, mimetype='application/json')


def similar_tasks():
    user = get_jwt_identity()
    tasks = TodoModel.query.filter_by(userID=user).all()
    similar_tasks_list = []
    index_of_similar_tasks = []
    for i in range(len(tasks)):
        sublists = []
        if i not in index_of_similar_tasks:
            sublists.append(tasks[i].id)
            for j in range(i+1, len(tasks)):
                if tasks[i].Description == tasks[j].Description:
                    sublists.append(tasks[j].id)
                    index_of_similar_tasks.append(j)
            if len(sublists) > 1:
                similar_tasks_list.append(sublists)
    message = []
    for similar_task in similar_tasks_list:
        sentence = "Task "
        sentence = sentence + ", Task ".join(map(str, similar_task[:-1]))
        sentence = sentence + f" and Task {similar_task[-1]} are similar tasks!"
        message.append(sentence)
    message = ', '.join(map(str, message))
    return Response(f'{{"message":"{message}"}}', status=status_codes.OK, mimetype='application/json')

