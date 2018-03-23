from flasgger import swag_from
from flask import Blueprint, request
from flask_restful import Api

from app.docs.sample import *
from app.views import BaseResource, json_required

api = Api(Blueprint('sample_api', __name__))
api.prefix = '/prefix'


@api.resource('/sample')
class Sample(BaseResource):
    @swag_from(SAMPLE_GET)
    @json_required('name', 'age')
    def get(self):
        return self.unicode_safe_json_dumps(request.json, 201)
