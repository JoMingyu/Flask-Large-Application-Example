import copy

from datetime import datetime
from unittest import TestCase as TC

import pymongo
from flask import Response
from redis import Redis

from app import create_app
from config.test import TestConfig


class TCBase(TC):
    def __init__(self, *args, **kwargs):
        self.app = create_app(TestConfig)

        mongo_setting = copy.copy(self.app.config['MONGODB_SETTINGS'])
        self.db_name = mongo_setting.pop('db')
        self.mongo_client = pymongo.MongoClient(**mongo_setting)

        self.redis_client = Redis(**self.app.config['REDIS_SETTINGS'])

        self.client = self.app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.token_regex = '([\w\-\_]+\.){2}[\w\-\_]+'

        super(TCBase, self).__init__(*args, **kwargs)

    def _create_fake_account(self):
        self.primary_user = None
        self.secondary_user = None

    def _generate_tokens(self):
        with self.app.app_context():
            self.primary_user_access_token = None
            self.primary_user_refresh_token = None
            self.secondary_user_access_token = None
            self.secondary_user_refresh_token = None

    def setUp(self):
        self._create_fake_account()
        self._generate_tokens()

    def tearDown(self):
        self.mongo_client.drop_database(self.db_name)
        self.redis_client.flushall()

    def request(self, method, target_url_rule, token=None, *args, **kwargs) -> Response:
        token = token or self.primary_user_access_token

        if not token.startswith('JWT'):
            token = 'JWT ' + token

        return method(
            target_url_rule,
            headers={'Authorization': token},
            *args,
            **kwargs
        )
