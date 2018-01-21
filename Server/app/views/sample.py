from flask_restful import Api
from flask import Blueprint

from app.views import BaseResource

sample_api = Api(Blueprint('sample_api', __name__))
sample_api.prefix = '/prefix'


@sample_api.resource('/sample')
class Sample(BaseResource):
    def get(self):
        return {
            'msg': 'hello!'
        }
