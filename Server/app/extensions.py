from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_validation import Validator
from flasgger import Swagger

cors = CORS()
jwt = JWTManager()
mongoengine = MongoEngine()
validator = Validator()
swagger = Swagger()

# jwt.user_loader_callback_loader(...)
# jwt.user_identity_loader(...)
