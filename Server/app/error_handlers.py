from flask import jsonify


def http_exception_handler(e):
    return jsonify({
        'msg': e.description
    }), e.code


def validation_error_handler(e):
    return jsonify({
        'msg': e.description
    }), 400


def broad_exception_error_handler(e):
    return jsonify({
        'msg': str(e),
    }), 500
