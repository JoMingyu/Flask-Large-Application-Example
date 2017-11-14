import os
import socket
from datetime import timedelta


class Config:
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 3003

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    # Secret key for any 3-rd party libraries

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # To turn off the track modifications of objects and signal emissions of Flask-SQLAlchemy
    # http://flask-sqlalchemy.pocoo.org/2.3/config

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=3)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=60)
    JWT_HEADER_TYPE = 'JWT'
    # http://flask-jwt-extended.readthedocs.io/en/latest/options.html

    API_VER = '1.0'
    API_TITLE = 'QuickStart from PlanB'
    API_DESC = '''
### [BASE URL] http://{0}:{1}

JWT Access Token의 유효기간은 {2}일, Refresh Token의 유효기간은 {3}일입니다.
    
- Status Code 1xx : Informational
- Status Code 2xx : Success
- Status Code 3xx : Redirection
- Status Code 4xx : Client Error
- Status Code 5xx : Server Error

##### <a href="https://httpstatuses.com/">[All of HTTP status code]</a>
##### <a href="http://meetup.toast.com/posts/92">[About REST API]</a>
##### <a href="http://jinja.pocoo.org/docs/2.10/">[About Jinja2]</a>
##### <a href="https://velopert.com/2389">[About JWT]</a>
    '''.format(HOST, PORT, JWT_ACCESS_TOKEN_EXPIRES.days, JWT_REFRESH_TOKEN_EXPIRES.days)
    # For flask-restful-swagger-2


class DevConfig(Config):
    DEBUG = True

    MONGODB_SETTINGS = {
        'db': 'quickstart.dev',
        'host': 'localhost',
    }
    # Port : default 27017


class ProductionConfig(Config):
    DEBUG = False

    MONGODB_SETTINGS = {
        'db': 'quickstart.production',
        'host': 'localhost',
    }
    # Port : default 27017


config = {
    'dev': DevConfig,
    'production': ProductionConfig
}
