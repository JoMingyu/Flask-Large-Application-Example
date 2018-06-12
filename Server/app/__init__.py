from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from redis import Redis
from influxdb import InfluxDBClient

from mongoengine import connect

from app.views import Router

WEB_FILE_ROOT_DIR = '../web_files'


def create_app(*config_cls) -> Flask:
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(
        __name__,
        # static_folder='{}/static'.format(WEB_FILE_ROOT_DIR),
        # template_folder='{}/templates'.format(WEB_FILE_ROOT_DIR)
    )

    for config in config_cls:
        app_.config.from_object(config)

    CORS().init_app(app_)
    JWTManager().init_app(app_)
    Swagger(template=app_.config['SWAGGER_TEMPLATE']).init_app(app_)
    Router().init_app(app_)

    connect(**app_.config['MONGODB_SETTINGS'])
    app_.config['REDIS_CLIENT'] = Redis(**app_.config['REDIS_SETTINGS'])
    app_.config['INFLUXDB_CLIENT'] = InfluxDBClient(**app_.config['INFLUXDB_SETTINGS'])

    cfg = app_.config

    if cfg['INFLUXDB_SETTINGS']['database'] not in cfg['INFLUXDB_CLIENT'].get_list_database():
        cfg['INFLUXDB_CLIENT'].create_database(cfg['INFLUXDB_SETTINGS']['database'])

    return app_
