from unittest import TestCase

from flask.wrappers import Response

from app import create_app
from config.app_config import LocalLevelConfig
from config.db_config import LocalDBConfig


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = create_app(LocalLevelConfig, LocalDBConfig)
        self.client = self.app.test_client()

        self.method = "GET"
        self.path = None
        self.path_parameters = dict()

        self.headers = dict()
        self.json = dict()
        self.query_string = dict()

    def request(self) -> Response:
        return self.client.open(
            method=self.method,
            path=self.path.format(**self.path_parameters),
            json=self.json,
            query_string=self.query_string,
        )
