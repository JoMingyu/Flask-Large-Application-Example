from flask_restful_swagger_2 import Api


class Swagger(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        settings = app.config['SWAGGER_SETTINGS']

        api = Api(
            app,
            api_spec_url=settings['API_VER'],
            title=settings['API_TITLE'],
            description=settings['API_DESC']
        )
