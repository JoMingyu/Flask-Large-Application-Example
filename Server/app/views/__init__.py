from functools import wraps
import ujson
import time

from flask import Response, request
from flask_restful import Resource, abort


def auth_required(fn):
    """
    View decorator for access control.

    ### TODO
    If you want to access control easily with this decorator,
    fill 'wrapper()' function included (1) aborting when access denied client (2) Set user object to flask.g

    - About custom view decorator
    -> http://flask-docs-kr.readthedocs.io/ko/latest/patterns/viewdecorators.html
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def json_required(*required_keys):
    """
    View decorator for JSON validation.

    - If content-type is not application/json : returns status code 406
    - If required_keys are not exist on request.json : returns status code 400

    :type required_keys: str
    """
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for required_key in required_keys:
                if required_key not in request.json:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    """
    BaseResource with some helper functions based flask_restful.Resource
    """
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs):
        """
        Helper function which processes json response with unicode using ujson

        :type data: dict or list
        :type status_code: int

        :rtype: Response
        """
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )


class Router(object):
    """
    REST resource routing helper class like standard flask 3-rd party libraries
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    @staticmethod
    def after_request(response):
        """
        Set header - X-Content-Type-Options=nosniff, X-Frame-Options=deny before response
        """
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'

        return response

    def init_app(self, app):
        """
        Routes resources. Use app.register_blueprint() aggressively
        """
        app.after_request(self.after_request)

        from app.views import sample
        app.register_blueprint(sample.api.blueprint)
