from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object(os.environ['APP_SETTINGS'])
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'register.login_user'
login_manager.login_message_category = 'info'
mail = Mail(app)
jwt= JWTManager(app)

from app.TasksManager.controllers import TasksManager
from app.UserManager.controllers import UserManager
app.register_blueprint(TasksManager)
app.register_blueprint(UserManager)

db.create_all()
