from functools import wraps
import ujson
import time

from flask import Response
from flask_restful import Resource, abort, request


def json_required(fn, required_keys=()):
    """
    View function with this decorator means
    "This view function required Content-Type=application/json in header"

    - If content-type is not application/json : returns status code 406
    - If required_keys are not exist on request.json : returns status code 400
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            abort(406)

        for required_key in required_keys:
            if required_key not in request.json:
                abort(400)

        return fn(*args, **kwargs)

    return wrapper


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_response(cls, data, status_code=200):
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8'
        )


class Router(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from app.views import sample
        app.register_blueprint(sample.api.blueprint)
