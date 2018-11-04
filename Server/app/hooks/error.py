from flask import jsonify


def http_exception_handler(e):
    return jsonify({
        'result': e.name,
        'hint': e.description
    }), e.code


def broad_exception_error_handler(e):
    return jsonify({
        'result': InternalServerError.description,
        'hint': str(e),
    }), 500
