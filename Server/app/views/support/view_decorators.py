from functools import wraps

from flask import request
from flask_restful import abort


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
