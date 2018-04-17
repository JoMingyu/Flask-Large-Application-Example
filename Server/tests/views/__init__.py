import ujson
from unittest import TestCase as TC

from flask import Response

from app import app


class TCBase(TC):
    def __init__(self, *args, **kwargs):
        self.client = app.test_client()

        super(TCBase, self).__init__(*args, **kwargs)

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

    def json_request(self, method, target_url_rule, token=None, *args, **kwargs):
        """
        Helper for json request

        Args:
            method (func): Request method
            target_url_rule (str): URL rule for request
            token (str) : JWT or OAuth's access token with prefix(Bearer, JWT, ...)

        Returns:
            Response
        """
        data = kwargs.pop('data')

        return method(
            target_url_rule,
            data=ujson.dumps(data) if data else None,
            content_type='application/json',
            headers={'Authorization': token or self.access_token},
            *args,
            **kwargs
        )

    def request(self, method, target_url_rule, token=None, *args, **kwargs):
        """
        Helper for common request

        Args:
            method (func): Request method
            target_url_rule (str): URL rule for request
            token (str) : JWT or OAuth's access token with prefix(Bearer, JWT, ...)

        Returns:
            Response
        """
        return method(
            target_url_rule,
            headers={'Authorization': token or self.access_token},
            *args,
            **kwargs
        )

    def decode_response_data(self, resp):
        return resp.data.decode()

    def get_response_data(self, resp):
        return ujson.loads(self.decode_response_data(resp))
