from flask import Flask
from redis import Redis

from mongoengine import connect

from app import extensions
from app.blueprints import api_v1_blueprint

# -- API load
from app.views import sample
# --


def register_extensions(app):
    extensions.swagger.template = app.config['SWAGGER_TEMPLATE']

    extensions.cors.init_app(app)
    extensions.jwt.init_app(app)
    extensions.validator.init_app(app)
    extensions.swagger.init_app(app)


def connect_databases(app):
    connect(**app.config['MONGODB_SETTINGS'])
    app.config['REDIS_CLIENT'] = Redis(**app.config['REDIS_SETTINGS'])


def register_blueprints(app):
    handle_exception_func = app.handle_exception
    handle_user_exception_func = app.handle_user_exception
    # register_blueprint 시 defer되었던 함수들이 호출되며, flask-restful.Api._init_app()이 호출되는데
    # 해당 메소드가 app 객체의 에러 핸들러를 오버라이딩해서, 별도로 적용한 handler의 HTTPException 관련 로직이 동작하지 않음
    # 따라서 두 함수를 임시 저장해 두고, register_blueprint 이후 함수를 재할당하도록 함

    app.register_blueprint(api_v1_blueprint)

    app.handle_exception = handle_exception_func
    app.handle_user_exception = handle_user_exception_func


def create_app(*config_cls) -> Flask:
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app = Flask(__name__)

    for config in config_cls:
        app.config.from_object(config)

    register_extensions(app)
    connect_databases(app)
    register_blueprints(app)

    return app
