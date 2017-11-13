from logging import INFO, Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask, current_app, request


def decorate(app):
    """
    :type app: Flask
    :rtype: None
    """
    @app.before_first_request
    def before_first_request():
        def make_logger():
            handler = RotatingFileHandler('server_log.log', maxBytes=100000, backupCount=5)
            handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s - %(message)s"))

            current_app.logger.addHandler(handler)
            current_app.logger.setLevel(INFO)

        make_logger()
        current_app.logger.info('------ Logger Initialized ------')

    @app.before_request
    def before_request():
        current_app.logger.info('Requested from {0} [ {1} {2} ]'.format(request.host, request.method, request.url))
        current_app.logger.info('Request values : {0}'.format(request.values))

    @app.after_request
    def after_request(response):
        current_app.logger.info('Respond : {0}'.format(response.status))

        response.headers['X-Powered-By'] = 'PlanB'
        response.headers['Content-Type'] = 'application/json; charset=utf8'
        # Fix encoding problem

        return response

    @app.teardown_appcontext
    def teardown_appcontext(exception):
        if not exception:
            current_app.logger.info('Teardown appcontext successfully.')
