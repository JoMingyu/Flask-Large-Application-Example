from datetime import datetime
from unittest import TestCase as TC

import pymongo
from flask import Response

from app import create_app
from config.test import TestConfig

app = create_app(TestConfig)


class TCBase(TC):
    mongo_setting = app.config['MONGODB_SETTINGS']
    db_name = mongo_setting.pop('db')
    mongo_client = pymongo.MongoClient(**mongo_setting)
    mongo_setting['db'] = db_name

    def __init__(self, *args, **kwargs):
        self.client = app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.token_regex = '(\w+\.){2}\w+'

        super(TCBase, self).__init__(*args, **kwargs)

    def _create_fake_account(self):
        self.primary_user = None
        self.secondary_user = None

    def _generate_tokens(self):
        with app.app_context():
            self.access_token = None
            self.refresh_token = None

    def setUp(self):
        self._create_fake_account()
        self._generate_tokens()

    def tearDown(self):
        self.mongo_client.drop_database(self.db_name)

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
