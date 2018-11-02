from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_validation import Validator
from flasgger import Swagger

cors = CORS()
jwt = JWTManager()
validator = Validator()
swagger = Swagger()
