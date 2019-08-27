from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException


def http_exception_handler(e: HTTPException):
    return jsonify({"message": e.description}), e.code


def broad_exception_handler(e: Exception):
    # TODO 에러를 세분화해서 잡는 것을 추천합니다.

    if current_app.debug:
        import traceback

        traceback.print_exc()

    return "", 500
