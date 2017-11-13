import pkgutil

from flask import Blueprint
from flask_restful_swagger_2 import Api

import config

from routes import api

cf = config.Config()


def _modules(packages):
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

_global_resources = set()


def _factory(packages, bp_endpoint, url_prefix='', api_spec_url='/api/swagger'):
    bp = Blueprint(bp_endpoint, __name__, url_prefix=url_prefix)
    api = Api(bp, api_spec_url=api_spec_url, api_version=cf.API_VER, title=cf.API_TITLE, description=cf.API_DESC)

    resources = set()

    for loader, name in _modules(packages):
        module_ = loader.find_module(name).load_module(name)
        try:
            for res in module_.Resource.__subclasses__():
                if res not in _global_resources:
                    resources.add(res)
                    _global_resources.add(res)
        except AttributeError:
            pass

    for res in resources:
        api.add_resource(res, res.uri)

    return bp

bp = _factory([api], 'API')

all_blueprints = (bp,)
