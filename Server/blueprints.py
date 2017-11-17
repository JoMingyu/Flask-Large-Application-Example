import pkgutil

from flask import Blueprint
from flask_restful_swagger_2 import Api

from app import views


class Blueprints:
    def __init__(self, app=None):
        self._global_resources = set()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        bp = self._factory(app, [views], 'API')

        all_blueprints = (bp,)

        for bp in all_blueprints:
            app.register_blueprint(bp)

    def _modules(self, packages):
        modules = set()

        def search(target):
            for loader, name, is_package in pkgutil.iter_modules(target.__path__):
                if is_package:
                    search(loader.find_module(name).load_module(name))
                else:
                    modules.add((loader, name))

        for pkg in packages:
            search(pkg)

        return modules

    def _factory(self, app, packages, bp_endpoint, url_prefix='', api_spec_url='/api/swagger'):
        bp = Blueprint(bp_endpoint, __name__, url_prefix=url_prefix)
        api = Api(bp, api_spec_url=api_spec_url, api_version=app.config['API_VER'], title=app.config['API_TITLE'], description=app.config['API_DESC'])

        resources = set()

        for loader, name in self._modules(packages):
            module_ = loader.find_module(name).load_module(name)
            try:
                for res in module_.Resource.__subclasses__():
                    if res not in self._global_resources:
                        resources.add(res)
                        self._global_resources.add(res)
            except AttributeError:
                pass

        for res in resources:
            api.add_resource(res, res.uri)

        return bp
