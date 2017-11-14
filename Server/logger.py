from logging import INFO, Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask, current_app, request


class Logger(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        :type app: Flask
        :rtype: None
        """
        def make_logger():
            handler = RotatingFileHandler('server_log.log', maxBytes=100000, backupCount=5)
            handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s - %(message)s"))

            current_app.logger.addHandler(handler)
            current_app.logger.setLevel(INFO)

            current_app.logger.info('------ Logger Initialized ------')

        def log_before_request():
            current_app.logger.info('Requested from {0} [ {1} {2} ]'.format(request.host, request.method, request.url))
            current_app.logger.info('Request values : {0}'.format(request.values))

        def log_after_request(response):
            current_app.logger.info('Respond : {0}'.format(response.status))

            response.headers['X-Powered-By'] = 'PlanB'
            response.headers['Content-Type'] = 'application/json; charset=utf8'
            # Fix encoding problem

            return response

        def log_teardown_appcontext(exception):
            if not exception:
                current_app.logger.info('Teardown appcontext successfully.')

        app.before_first_request(make_logger)
        app.before_request(log_before_request)
        app.after_request(log_after_request)
        app.teardown_appcontext(log_teardown_appcontext)
