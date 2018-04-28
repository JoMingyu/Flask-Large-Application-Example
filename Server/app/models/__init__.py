from mongoengine import *


class Mongo:
    """
    MongoDB connection helper class like standard flask 3-rd party libraries
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        setting = app.config['MONGODB_SETTINGS']

        connect(**setting)
        print('[INFO] MongoEngine initialized with {}'.format(setting))
