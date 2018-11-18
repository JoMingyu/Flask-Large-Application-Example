from flask import jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import InternalServerError


def http_exception_handler(e: HTTPException):
    return jsonify({
        'result': e.name,
        'hint': e.description
    }), e.code


def broad_exception_error_handler(e: Exception):
    return jsonify({
        'result': InternalServerError.description,
        'hint': str(e),
    }), 500
