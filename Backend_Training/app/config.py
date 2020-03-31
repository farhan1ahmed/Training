import os
class BaseConfig(object):
    DEBUG = True
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = b'5791628bb0b13ce0c676dfde280ba245'
    PASSWORD_SALT = b'6dfde280ba245'
    JWT_TOKEN = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
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


