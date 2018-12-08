import json
from typing import Union, List, Dict

from flask import Flask, Response
from flask_restful import Api, Resource

from app.blueprints import api_v1_blueprint


class BaseResource(Resource):
    @classmethod
    def unicode_safe_json_dumps(cls, data: Union[List, Dict], status_code: int=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )


def route(flask_app: Flask):
    from app.views.sample import sample
    # circular import 방어

    api_v1 = Api(api_v1_blueprint)

    api_v1.add_resource(sample.Sample, '/sample')

    flask_app.register_blueprint(api_v1_blueprint)
