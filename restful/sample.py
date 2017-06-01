from flask import request
from flask_restful import Resource


class Sample(Resource):
    def post(self):
        data = request.form['test_form']

        return '', 201
