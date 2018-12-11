from flask import Blueprint, Flask


def route(flask_app: Flask):
    from app.views.sample import sample

    api_v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

    api_v1_blueprint.add_url_rule('/sample', view_func=sample.Sample.as_view('sample'))

    flask_app.register_blueprint(api_v1_blueprint)
