import ujson
import time

from flask import Response
from flask_restful import Resource


class BaseResource(Resource):
    """
    BaseResource with some helper functions based flask_restful.Resource
    """
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_response(cls, data, status_code=200):
        """
        Helper function which processes json response with unicode using ujson

        - About ujson.dumps(data, ensure_ascii=False)
        If ensure_ascii is true (the default),
        all non-ASCII characters in the output are escaped with \\uXXXX sequences,
        and the result is a str instance consisting of ASCII characters only.

        If ensure_ascii is false, some chunks written to fp may be unicode instances.

        :type data: dict or list
        :type status_code: int

        :rtype: Response
        """
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8'
        )