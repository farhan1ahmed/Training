from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object('config')
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'register.login_user'
login_manager.login_message_category = 'info'

from app.mod_webapp.controllers import mod_webapp
from app.mod_usercreation_login.controllers import mod_register_login
app.register_blueprint(mod_webapp)
app.register_blueprint(mod_register_login)

db.create_all()
