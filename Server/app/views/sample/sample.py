from flasgger import swag_from
from flask import jsonify, request
from flask.views import MethodView
from flask_validation import validate_with_jsonschema

from app.docs.sample import *


class Sample(MethodView):
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

        return jsonify(payload), 201
