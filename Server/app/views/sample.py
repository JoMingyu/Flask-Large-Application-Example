from flasgger import swag_from
from flask import request
from flask_restful import Api
from flask_validation import validate_keys

from app.docs.sample import *
from app.views import BaseResource, api_v1_blueprint

api = Api(api_v1_blueprint)
api.prefix = '/prefix'


@api.resource('/sample')
class Sample(BaseResource):
    @swag_from(SAMPLE_POST)
    @validate_keys(('age', 'name'))
    def post(self):
        payload = request.json

        return self.unicode_safe_json_dumps(payload, 201)
