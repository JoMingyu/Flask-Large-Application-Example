import ujson
from unittest import TestCase as TC

from flask import Response

from app import app


class TCBase(TC):
    def __init__(self, *args, **kwargs):
        TC.__init__(self, *args, **kwargs)

        self.client = app.test_client()

    def _create_fake_account(self):
        pass

    def _get_tokens(self):
        self.access_token = None
        self.refresh_token = None

    def setUp(self):
        self._create_fake_account()
        self._get_tokens()

    def tearDown(self):
        pass

    def json_request(self, method, target_url_rule, query_string=None, data=None, token=None, *args, **kwargs):
        """
        Helper for json request

        Args:
            method (func): Request method
            target_url_rule (str): URL rule for request
            query_string (dict): Query parameters
            data (dict): JSON payload (application/json)
            token (str) : JWT or OAuth's access token with prefix(Bearer, JWT, ...)

        Returns:
            Response
        """
        if token is None:
            token = self.access_token

        return method(
            target_url_rule,
            query_string=query_string,
            data=ujson.dumps(data) if data else None,
            content_type='application/json',
            headers={'Authorization': token},
            *args,
            **kwargs
        )

    def request(self, method, target_url_rule, query_string=None, data=None, token=None, *args, **kwargs):
        """
        Helper for common request

        Args:
            method (func): Request method
            target_url_rule (str): URL rule for request
            query_string (dict): Query parameters
            data (dict): Body parameters (application/x-www-form-urlencoded)
            token (str) : JWT or OAuth's access token with prefix(Bearer, JWT, ...)

        Returns:
            Response
        """
        if token is None:
            token = self.access_token

        return method(
            target_url_rule,
            query_string=query_string,
            data=data,
            headers={'Authorization': token},
            *args,
            **kwargs
        )

    def get_response_data(self, resp):
        return ujson.loads(resp.data.decode())
