from flask import Flask
from flask_restful import Api

from app.blueprints import api_v1_blueprint


def route(flask_app: Flask):
    from app.views.sample import sample

    api_v1 = Api(api_v1_blueprint)

    api_v1.add_resource(sample.Sample, '/sample')

    flask_app.register_blueprint(api_v1_blueprint)
