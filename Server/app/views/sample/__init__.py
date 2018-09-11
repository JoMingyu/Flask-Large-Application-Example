from flask_restful import Api

from app.blueprints import api_v1_blueprint
from app.views.sample import sample

api = Api(api_v1_blueprint, prefix='/sample')

api.add_resource(sample.Sample, '/echo')
# 이 모듈의 api 객체를 가져가 @api.resource()하는 경우 URL rule이 퍼져 있는 범위가 넓어서 찾기 힘듬
