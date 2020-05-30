import os
class BaseConfig(object):
    DEBUG = True
    SERVER_NAME = 'localhost:5000'
    SESSION_COOKIE_DOMAIN = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PASSWORD_SALT = os.environ.get('PASSWORD_SALT')
    JWT_TOKEN = os.environ.get('JWT_TOKEN')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'

    #Mail Setting
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    DEFAULT_MAIL_SENDER = os.environ.get('DEFAULT_MAIL_SENDER')

    # gmail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

    # Facebook
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')


class TestConfig(BaseConfig):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
