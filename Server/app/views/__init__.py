import json
from typing import Union, List, Dict

from flask import Response
from flask_restful import Resource


class BaseResource(Resource):
    @classmethod
    def unicode_safe_json_dumps(cls, data: Union[List, Dict], status_code: int=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )
