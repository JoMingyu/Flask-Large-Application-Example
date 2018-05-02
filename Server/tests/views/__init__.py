from datetime import datetime
from unittest import TestCase as TC

import pymongo
import ujson
from flask import Response

from app import create_app
from config.test import TestConfig

app = create_app(TestConfig)

mongo_setting = app.config['MONGODB_SETTINGS']
db_name = mongo_setting.pop('db')
mongo_client = pymongo.MongoClient(mongo_setting)


class TCBase(TC):
    def __init__(self, *args, **kwargs):
        self.client = app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')

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
        mongo_client.drop_database(db_name)

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

    def get_response_data_as_json(self, resp):
        return ujson.loads(self.decode_response_data(resp))
