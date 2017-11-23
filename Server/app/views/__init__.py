from flask_restful_swagger_2 import Api
from flask_restful import Api
from flasgger import Swagger

from app.docs import TEMPLATE


class ViewInjector(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        Swagger(app, template=TEMPLATE)

        api = Api(app)
