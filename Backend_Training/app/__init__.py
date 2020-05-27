from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
import os
import atexit
import logging

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object(os.environ['APP_SETTINGS'])
bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)

logging.basicConfig(level=logging.DEBUG)
file_handler = logging.FileHandler('todo.log')
LOG_LEVEL = os.environ.get('LOG_SEVERITY_LEVEL', 'INFO')
file_handler.setLevel(level=LOG_LEVEL)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logging.getLogger().addHandler(file_handler)


from app.tasks.controllers import tasks
from app.users.controllers import users
app.register_blueprint(tasks)
app.register_blueprint(users)

db.create_all()

from app.utils.task_reminder_email import mail_reminder
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    mail_scheduler = BackgroundScheduler()
    mail_scheduler.configure(timezone='utc')
    mail_scheduler.add_job(mail_reminder, trigger='interval', days=1, start_date='2020-01-01 00:00:00')
    mail_scheduler.start()


def shutdown(): mail_scheduler.shutdown(wait=False)


atexit.register(shutdown)

