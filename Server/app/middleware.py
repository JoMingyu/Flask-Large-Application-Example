from logging import INFO, Formatter
from logging.handlers import RotatingFileHandler

from flask import current_app, request, render_template


class Logger(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.before_first_request
        def make_logger():
            handler = RotatingFileHandler('server_log.log', maxBytes=100000, backupCount=5)
            handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s - %(message)s"))

            current_app.logger.addHandler(handler)
            current_app.logger.setLevel(INFO)

            current_app.logger.info('------ Logger Initialized ------')

        @app.before_request
        def before_request():
            current_app.logger.info('Requested from {0} [ {1} {2} ]'.format(request.host, request.method, request.url))
            current_app.logger.info('Request values : {0}'.format(request.values))

        @app.after_request
        def after_request(response):
            current_app.logger.info('Respond : {0}'.format(response.status))

            response.headers['X-Powered-By'] = app.config['SERVICE_NAME']

            return response

        @app.teardown_appcontext
        def teardown_appcontext(exception):
            if not exception:
                current_app.logger.info('Teardown appcontext successfully.')


class ErrorHandler(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.errorhandler(403)
        def handler_403(e):
            return render_template('403.html'), 403

        @app.errorhandler(404)
        def handler_404(e):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def handler_500(e):
            return render_template('500.html'), 500
