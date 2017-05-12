from flask import request
from flask_restful import Resource


class Sample(Resource):
    def get(self):
        param = request.args.get('test_param')
        return param, 200

    def post(self):
        form_att = request.form['test_form']
        data = {
            'received_value': form_att
        }
        return data, 201
