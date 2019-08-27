from app.context import context_property
from config.app_config import LocalLevelConfig
from tests import BaseTestCase


class TestContextProperty(BaseTestCase):
    def test_secret_key(self):
        """
        request context 내에서 secret key 접근
        """

        with self.app.test_request_context():
            self.assertEqual(LocalLevelConfig.SECRET_KEY, context_property.secret_key)

    def test_secret_key_raise_runtime_error_on_outside_context(self):
        """
        request context 밖에서 secret key 접근 시 RuntimeError 발생
        """

        with self.assertRaises(RuntimeError):
            _ = context_property.secret_key

    def test_request_payload_without_set(self):
        """
        request context 내에서 임의의 값이 set되지 않은 request payload 접근
        -> None으로 평가되어야 함
        """

        with self.app.test_request_context():
            self.assertIsNone(context_property.request_payload)

    def test_request_payload_with_set(self):
        """
        request context 내에서 임의의 값이 set된 request payload 접근
        -> set된 값이 반환되어야 함
        """

        with self.app.test_request_context():
            context_property.request_payload = 0

            self.assertEqual(0, context_property.request_payload)

    def test_request_payload_raise_runtime_error_on_outside_context(self):
        """
        request context 밖에서 request payload 접근 시 RuntimeError 발생
        """

        with self.assertRaises(RuntimeError):
            context_property.request_payload = 0
            _ = context_property.request_payload
