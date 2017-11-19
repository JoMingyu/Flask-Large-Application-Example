from flask_restful_swagger_2 import Api


class Swagger(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        api = Api(
            app,
            api_spec_url=app.config['API_VER'],
            title=app.config['API_TITLE'],
            description=app.config['API_DESC']
        )
