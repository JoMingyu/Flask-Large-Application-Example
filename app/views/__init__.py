from flask import Blueprint, Flask
from flask_restful import Api


def route(flask_app: Flask):
    from app.views.sample import sample

    api_v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

    api_v1 = Api(api_v1_blueprint)

    api_v1.add_resource(sample.Sample, '/sample')

    flask_app.register_blueprint(api_v1_blueprint)
