import json
import time

from flask import Blueprint, Response
from flask_restful import Resource
from werkzeug.exceptions import HTTPException

from app import errorhandlers, request_callback_decorators

api_v1_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api_v1_blueprint.register_error_handler(HTTPException, errorhandlers.http_exception_handler)
api_v1_blueprint.register_error_handler(Exception, errorhandlers.broad_exception_error_handler)
api_v1_blueprint.after_request(request_callback_decorators.after_request)


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )
