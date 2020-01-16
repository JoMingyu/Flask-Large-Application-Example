import json
from http import HTTPStatus

from flask import current_app, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException


def broad_exception_handler(e: Exception):
    # TODO 에러를 세분화해서 잡는 것을 추천합니다.

    if isinstance(e, HTTPException):
        message = e.description
        code = e.code

    elif isinstance(e, ValidationError):
        message = json.loads(e.json())
        code = HTTPStatus.BAD_REQUEST

    else:
        message = ""
        code = HTTPStatus.INTERNAL_SERVER_ERROR

        if current_app.debug:
            import traceback

            traceback.print_exc()

    return jsonify({"error": message}), code
