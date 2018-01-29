from flask_restful import Api
from flask import Blueprint

from app.views import BaseResource

api = Api(Blueprint('sample_api', __name__))
api.prefix = '/prefix'


@api.resource('/sample')
class Sample(BaseResource):
    def get(self):
        return json_response({
            'at': self.now,
            'msg': 'hello!'
        })
