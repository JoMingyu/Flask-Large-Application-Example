from flasgger import swag_from
from flask import Blueprint
from flask_restful import Api

from app.docs.sample import *
from app.views import BaseResource

api = Api(Blueprint('sample_api', __name__))
api.prefix = '/prefix'


@api.resource('/sample')
class Sample(BaseResource):
    @swag_from(SAMPLE_GET)
    def get(self):
        return self.unicode_safe_json_response({
            'at': self.now,
            'msg': 'hello!'
        })
