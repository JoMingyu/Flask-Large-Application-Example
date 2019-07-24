from abc import abstractmethod

from flask import g

from app.context import _ContextLocalData
from tests import BaseTestCase


class TestContextLocalData(BaseTestCase):
    def setUp(self):
        super(TestContextLocalData, self).setUp()

        self.test_context_local_data = _ContextLocalData("test", None)

    @property
    @abstractmethod
    def proxy_object(self):
        pass

    def _test_set(self):
        """
        set 테스트
        """

        with self.app.test_request_context():
            self.test_context_local_data.set(self.proxy_object, 0)
            self.assertEqual(0, self.proxy_object.test)

    def _test_set_outside_context(self):
        """
        context 바깥에서의 set 테스트
        """

        with self.assertRaises(RuntimeError):
            self.test_context_local_data.set(self.proxy_object, 0)

    def _test_get(self):
        """
        get 테스트
        """

        with self.app.test_request_context():
            self.proxy_object.test = 0
            self.assertEqual(0, self.test_context_local_data.get(self.proxy_object))

    def _test_get_outside_context(self):
        """
        context 바깥에서의 get 테스트
        """

        with self.assertRaises(RuntimeError):
            _ = self.test_context_local_data.get(self.proxy_object)

    def _test_get_default_value(self):
        """
        get의 기본값 반환 테스트
        """

        with self.app.test_request_context():
            self.assertEqual(None, self.test_context_local_data.get(self.proxy_object))


class TestContextLocalDataOnGObject(TestContextLocalData):
    @property
    def proxy_object(self):
        return g

    def test_set(self):
        self._test_set()

    def test_set_outside_context(self):
        self._test_set_outside_context()

    def test_get(self):
        self._test_get()

    def test_get_outside_context(self):
        self._test_get_outside_context()

    def test_get_default_value(self):
        self._test_get_default_value()
