from mongoengine import *


class Mongo(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        settings = app.config['MONGODB_SETTINGS']

        connect(
            db=settings.get('db'),
            host=settings.get('host'),
            port=settings.get('port'),
            username=settings.get('username'),
            password=settings.get('password')
        )
