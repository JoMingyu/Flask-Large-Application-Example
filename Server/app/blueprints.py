from flask import Blueprint
from werkzeug.exceptions import HTTPException

from app import errorhandlers

api_v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api_v1_blueprint.register_error_handler(HTTPException, errorhandlers.http_exception_handler)
api_v1_blueprint.register_error_handler(Exception, errorhandlers.broad_exception_error_handler)
