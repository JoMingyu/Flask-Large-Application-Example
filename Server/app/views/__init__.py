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
        def route(modules, url_prefix=None):
            for module in modules:
                app.register_blueprint(module.api.blueprint, url_prefix=url_prefix)

        from app.views.sample import sample_api
        route(sample_api)
