import pytest
import sys
import os
sys.path.append('C:\\Users\\hp\\PycharmProjects\\Training\\Backend_Training')
from app.users.models import UserModel
from app.tasks.models import TodoModel
from app.utils.date_parser import get_date
from flask import Flask
from app import db as test_db
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import datetime


test_app = Flask(__name__)
test_app.config.from_object(os.environ.get('TEST_SETTINGS'))
test_db.init_app(test_app)
Bcrypt(test_app)
Mail(test_app)
JWTManager(test_app)
from app.tasks.controllers import tasks
from app.users.controllers import users
test_app.register_blueprint(tasks)
test_app.register_blueprint(users)


@pytest.fixture
def make_new_user():
    username = "test_user"
    email = "test_user@gmail.com"
    password = "test123"
    new_user = UserModel(username, email, password)
    return new_user


@pytest.fixture
def make_new_task():
    title = "Test Task"
    description = "Run test for new task"
    duedate = get_date("2020-08-12")
    new_task = TodoModel(Title=title, Description=description, DueDate=duedate)
    return new_task


@pytest.fixture
def test_client():
    client = test_app.test_client()

    with test_app.app_context():
        from app.users.models import UserModel
        test_db.create_all()
        test_db.session.commit()
        test_user_1 = UserModel(username="Test_User_1", email="farhan1ahmed@hotmail.com", password="test123")
        test_user_1.confirmed = True
        task_1 = TodoModel(Title="Task 1", Description="Test Task 1", DueDate=get_date("2020-07-11"), userID=1)
        task_2 = TodoModel(Title="Task 2", Description="Test Task 2", DueDate=get_date("2020-05-11"), userID=1)
        task_3 = TodoModel(Title="Task 3", Description="Test Task 3", DueDate=get_date("2020-06-11"), userID=1,
                           Status_id=3, CompletionDate=datetime.datetime.utcnow().date())
        test_db.session.add(test_user_1)
        test_db.session.add(task_1)
        test_db.session.add(task_2)
        test_db.session.add(task_3)
        test_user_2 = UserModel(username="Test_User_2", email="farhan313ahmed@gmail.com", password="pass123")
        test_user_2.confirmed = True
        task_1 = TodoModel(Title="Task 1", Description="Test Task 1", DueDate=get_date("2020-08-11"), userID=2)
        task_2 = TodoModel(Title="Task 2", Description="Test Task 2", DueDate=get_date("2020-04-11"), userID=2,
                           Status_id=3, CompletionDate=datetime.datetime.utcnow().date())
        test_db.session.add(test_user_2)
        test_db.session.add(task_1)
        test_db.session.add(task_2)
        test_db.session.commit()
        yield client
        test_db.session.remove()
        test_db.drop_all()

