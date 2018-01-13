import time

from flask_restful import Resource


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')


class ViewInjector(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        from app.views.sample import sample_api
        app.register_blueprint(sample_api)
