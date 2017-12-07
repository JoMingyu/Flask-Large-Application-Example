from mongoengine import *


class Mongo(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        connect(app.config['MONGODB_SETTINGS']['db'])
