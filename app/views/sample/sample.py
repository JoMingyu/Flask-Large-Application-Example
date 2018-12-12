from flask import request
from flask_restful import Resource

from app.decorators.json_validator import validate_with_jsonschema


class Sample(Resource):
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
