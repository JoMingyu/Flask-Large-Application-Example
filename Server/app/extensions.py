from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_validation import Validator

cors = CORS()
jwt = JWTManager()
validator = Validator()
