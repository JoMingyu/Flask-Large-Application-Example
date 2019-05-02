from flask import current_app
from werkzeug.exceptions import HTTPException


def http_exception_handler(e: HTTPException):
    return '', e.code


def broad_exception_handler(e: Exception):
    if current_app.debug:
        import traceback
        traceback.print_exc()

    return '', 500
