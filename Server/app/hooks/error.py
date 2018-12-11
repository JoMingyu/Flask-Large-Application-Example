from werkzeug.exceptions import HTTPException


def http_exception_handler(e: HTTPException):
    return '', e.code


def broad_exception_error_handler(e: Exception):
    return '', 500
