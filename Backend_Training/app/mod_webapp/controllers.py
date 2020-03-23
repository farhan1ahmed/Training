from flask import json, Blueprint, request, render_template, flash, redirect, url_for
from app.mod_webapp.helper import ToDoHelper
from flask_login import login_required, current_user
from .forms import CreateTaskForm
from app import db
from app.database_structure import TodoModel

mod_webapp = Blueprint('webapp', __name__)
@mod_webapp.route("/hello")
@login_required
def hello():
    return "Hello World!"

@mod_webapp.route("/home")
@login_required
def home():
    tasks = TodoModel.query.filter_by(user=current_user).all()
    print(tasks)
    return str(tasks)


@mod_webapp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = CreateTaskForm()
    if form.validate_on_submit():
        print(type(form.DueDate.data))
        todo = TodoModel(Title=form.Title.data, Description=form.Description.data, DueDate=form.DueDate.data, user=current_user)
        db.session.add(todo)
        db.session.commit()
        flash('Task Created!')
        return redirect(url_for('webapp.home'))
    return render_template('create_task.html', title='New Task', form=form)