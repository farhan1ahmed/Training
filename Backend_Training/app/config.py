import os
class BaseConfig(object):
    DEBUG = True
    SERVER_NAME = '127.0.0.1:5000'
    SESSION_COOKIE_DOMAIN = False

    SECRET_KEY = os.environ['SECRET_KEY']
    PASSWORD_SALT = os.environ['PASSWORD_SALT']
    JWT_TOKEN = os.environ['JWT_TOKEN']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'

    #Mail Setting
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    DEFAULT_MAIL_SENDER = 'farhan313ahmed@gmail.com'

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']


