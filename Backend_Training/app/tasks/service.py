from flask import Response, json
from flask_jwt_extended import get_jwt_identity
import datetime, os
from .models import TodoModel
from app import db
from app.utils import status_codes
from app.utils.date_parser import get_date
from sqlalchemy import exc, not_


TITLE = 'Title'
DESCRIPTION = 'Description'
DUE_DATE = 'DueDate'
STATUS = 'Status'
STATUS_ID = 'Status_id'
COMPLETED = 3
CACHE_DICTIONARY = dict()
BASE_URL = "localhost:5000/reports"

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

    due_date = get_date(request_body.get(DUE_DATE))
    task = TodoModel(Title=request_body.get(TITLE), Description=request_body.get(DESCRIPTION), DueDate=due_date,
                     userID=get_jwt_identity(), Status_id=request_body.get(STATUS_ID))
    try:
        db.session.add(task)
        db.session.commit()
    except exc.IntegrityError as exception:
        return Response(f'{{"message": "{exception}"}}', status=status_codes.CONFLICT, mimetype='application/json')
    return Response('{"message":"success"}', status=status_codes.CREATED, mimetype='application/json')


def list_all_items(request):
    user = get_jwt_identity()
    tasks = get_paginated_list(user, start=int(request.args.get('start', 1)), limit=int(request.args.get('limit', 5)))
    return tasks


def get_paginated_list(user, start, limit):
    tasks = TodoModel.query.filter_by(userID=user).offset(start-1).limit(limit).all()
    total_tasks = TodoModel.query.filter_by(userID=user).count()
    if start > total_tasks:
        return Response('{"message":"Page not found"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    response_object = {}
    # tasks for current page
    page_tasks = [task.list_all for task in tasks]
    response_object['tasks'] = page_tasks
    url = '/list_items/page'
    response_object['start'] = start
    response_object['limit'] = limit
    response_object['total_tasks'] = total_tasks
    # set previous url
    if start == 1:
        response_object['previous'] = ''
    else:
        start_of_previous_page = max(1, start-limit)
        end_of_previous_page = start - 1
        response_object['previous'] = url + f'?start={start_of_previous_page}&limit={end_of_previous_page}'
    # set next url
    if start + limit > total_tasks:
        response_object['next'] = ''
    else:
        start_of_next_page= start + limit
        response_object['next'] = url + f'?start={start_of_next_page}&limit={limit}'
    return Response(json.dumps(response_object), status=status_codes.OK, mimetype='application/json')



def list_item(item_id):
    user = get_jwt_identity()
    task = TodoModel.query.filter_by(userID=user).filter_by(id=item_id).first()
    if task is None:
        return Response('{"message":"No Content"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    return Response(json.dumps(task.list_all), status=status_codes.OK, mimetype='application/json')


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
    for attribute in request_body:
        if attribute == DUE_DATE:
            due_date = get_date(request_body.get(DUE_DATE))
            setattr(task, attribute, due_date)
        else:
            setattr(task, attribute, request_body.get(attribute))
    if task.Status_id == COMPLETED:
        task.CompletionDate = datetime.datetime.utcnow()
    try:
        db.session.commit()
    except exc.IntegrityError:
        return Response(f'{{"message": "{exc.IntegrityError}"}}', status=status_codes.CONFLICT,
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
        return Response('{"message":"No Task Found"}', status=status_codes.NOT_FOUND, mimetype='application/json')
    if task.Attachment_data is None and task.Attachment_name is None:
        return Response('{"message":"No Attachment Found"}', status=status_codes.NOT_FOUND, mimetype='application/json')
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
    dict_task = {}
    for task in tasks:
        dict_task.setdefault(task.Description, []).append(task.id)
    message = []
    for key in dict_task:
        if len(dict_task.get(key)) > 1:
            sentence = "Task "
            sentence = sentence + ", Task ".join(map(str, dict_task.get(key)[:-1]))
            sentence = sentence + f" and Task {dict_task.get(key)[-1]} are similar tasks!"
            message.append(sentence)
    return Response(f'{{"message":"{message}"}}', status=status_codes.OK, mimetype='application/json')


def tasks_opened_week():
    user = get_jwt_identity()
    url_endpoint = BASE_URL + "/tasks_opened_week"
    cached_response = cache_dictionary(user, url_endpoint)
    if cached_response:
        print("Cached")
        return Response(json.dumps(cached_response), status=status_codes.OK, mimetype='application/json')
    tasks = TodoModel.query.filter_by(userID=user).all()
    if len(tasks) == 0:
        return Response("message: No tasks found", status=status_codes.NOT_FOUND, mimetype='application/json')
    week = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    for task in tasks:
        day = task.CreationDate.strftime("%A")
        if day in week:
            week[day] += 1
    print("Non-Cached")
    CACHE_DICTIONARY[user][url_endpoint] = [week, datetime.datetime.utcnow()]
    return Response(json.dumps(week), status=status_codes.OK, mimetype='application/json')


def max_tasks_day():
    user = get_jwt_identity()
    url_endpoint = BASE_URL + "/max_tasks_day"
    cached_response = cache_dictionary(user, url_endpoint)
    if cached_response:
        print("Cached")
        return Response(json.dumps(cached_response), status=status_codes.OK, mimetype='application/json')
    tasks = TodoModel.query.filter_by(userID=user).filter_by(Status_id=COMPLETED).all()
    if len(tasks) == 0:
        return Response("message: No tasks found", status=status_codes.NOT_FOUND, mimetype='application/json')
    completed_task_dict = dict()
    for task in tasks:
        completed_task_dict.setdefault(task.CompletionDate.date(), []).append(task.id)
    max_tasks = 0
    for key in completed_task_dict:
        if len(completed_task_dict.get(key)) > max_tasks:
            max_tasks = len(completed_task_dict.get(key))
            resp_obj = dict()
            resp_obj["max_count"] = max_tasks
            resp_obj.setdefault("date", []).append(key)
        elif len(completed_task_dict.get(key)) == max_tasks:
            resp_obj.setdefault("date", []).append(key)
    print("Non-Cached")
    CACHE_DICTIONARY[user][url_endpoint] = [resp_obj, datetime.datetime.utcnow()]
    return Response(json.dumps(resp_obj), status=status_codes.OK, mimetype='application/json')


def late_tasks():
    user = get_jwt_identity()
    url_endpoint = BASE_URL + "/late_tasks"
    cached_response = cache_dictionary(user, url_endpoint)
    if cached_response:
        print("Cached")
        return Response(json.dumps(cached_response), status=status_codes.OK, mimetype='application/json')
    tasks = TodoModel.query.filter_by(userID=user).all()
    if len(tasks) == 0:
        return Response("message: No tasks found", status=status_codes.NOT_FOUND, mimetype='application/json')
    count = 0
    for task in tasks:
        if task.CompletionDate is None:
            if task.DueDate.date() < datetime.date.today():
                count = count + 1
        elif task.DueDate.date() < task.CompletionDate.date():
            count = count + 1
    resp_obj = dict()
    resp_obj["count"] = count
    print("Non-Cached")
    CACHE_DICTIONARY[user][url_endpoint] = [resp_obj, datetime.datetime.utcnow()]
    return Response(json.dumps(resp_obj), status=status_codes.OK, mimetype='application/json')


def avg_tasks_per_day():
    user = get_jwt_identity()
    url_endpoint = BASE_URL + "/avg_tasks_per_day"
    cached_response = cache_dictionary(user, url_endpoint)
    if cached_response:
        print("Cached")
        return Response(json.dumps(cached_response), status=status_codes.OK, mimetype='application/json')
    completed_tasks = TodoModel.query.filter_by(userID=user).filter_by(Status_id=3).count()
    first_task = TodoModel.query.filter_by(userID=user).order_by(TodoModel.CreationDate).first()
    if first_task is None:
        return Response("message: No tasks found", status=status_codes.NOT_FOUND, mimetype='application/json')
    start_date = first_task.CreationDate
    today = datetime.date.today()
    no_of_days = int((today - start_date.date()).days)
    avg_tasks_completed = completed_tasks / no_of_days
    resp_obj = dict()
    resp_obj["avg_tasks"] = avg_tasks_completed
    print("Non-Cached")
    CACHE_DICTIONARY[user][url_endpoint] = [resp_obj, datetime.datetime.utcnow()]
    return Response(json.dumps(resp_obj), status=status_codes.OK, mimetype='application/json')


def tasks_count_breakdown():
    user = get_jwt_identity()
    url_endpoint = BASE_URL + "/tasks_count_breakdown"
    cached_response = cache_dictionary(user, url_endpoint)
    if cached_response:
        print("Cached")
        return Response(json.dumps(cached_response), status=status_codes.OK, mimetype='application/json')
    total_tasks = TodoModel.query.filter_by(userID=user).count()
    if total_tasks == 0:
        return Response("message: No task found", status=status_codes.NOT_FOUND, mimetype='application/json')
    completed_tasks = TodoModel.query.filter_by(userID=user).filter_by(Status_id=COMPLETED).count()
    remaining_tasks = TodoModel.query.filter_by(userID=user). filter(not_(TodoModel.Status_id.like(COMPLETED))).count()
    resp_obj = dict()
    resp_obj['total_tasks'] = total_tasks
    resp_obj['completed_tasks'] = completed_tasks
    resp_obj['remaining_tasks'] = remaining_tasks
    print("Non-Cached")
    CACHE_DICTIONARY[user][url_endpoint] = [resp_obj, datetime.datetime.utcnow()]
    return Response(json.dumps(resp_obj), status=status_codes.OK, mimetype='application/json')


def cache_dictionary(user, url):
    user_dict = CACHE_DICTIONARY.get(user)
    if user_dict:
        if user_dict.get(url):
            content = user_dict.get(url)[0]
            last_time = user_dict.get(url)[1]
            if (datetime.datetime.utcnow() - last_time).seconds <= 900:
                return content
            else:
                del user_dict[url]
                return None
    else:
        CACHE_DICTIONARY[user] = dict()
        return None
