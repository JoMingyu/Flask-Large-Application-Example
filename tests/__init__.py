from unittest import TestCase

from app import create_app
from config.app_config import LocalLevelConfig
from config.db_config import LocalDBConfig


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = create_app(LocalLevelConfig, LocalDBConfig)
        self.client = self.app.test_client()
