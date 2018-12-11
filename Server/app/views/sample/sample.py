from flasgger import swag_from
from flask import request
from flask_restful import Resource
from flask_validation import validate_with_jsonschema

from app.docs.sample import *


class Sample(Resource):
    @swag_from(SAMPLE_POST)
    @validate_with_jsonschema({
        'type': 'object',
        'required': ['age', 'name'],
        'properties': {
            'age': {
                'type': 'integer',
                'minimum': 0
            },
            'name': {
                'type': 'string'
            }
        }
    })
    def post(self):
        payload = request.json

        return self.unicode_safe_json_dumps(payload, 201)
