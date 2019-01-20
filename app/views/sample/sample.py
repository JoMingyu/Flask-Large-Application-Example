from flask import request

from app.decorators.json_validator import validate_with_jsonschema
from app.views.base import BaseResource


class Sample(BaseResource):
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

        return payload, 201
