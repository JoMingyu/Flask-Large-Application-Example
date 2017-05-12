from flask import Flask
from flask_restful import Api
from restful_modules import sample


app = Flask(__name__)
api = Api(app)

api.add_resource(sample.Sample, '/sample')


if '__main__' == __name__:
    app.run(host='0.0.0.0', port=80)
