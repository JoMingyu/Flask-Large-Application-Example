from abc import abstractmethod

from flask import g

from app.context import _ContextLocalData
from tests import BaseTestCase


class TestContextLocalData(BaseTestCase):
    def setUp(self):
        """
        Sets the test context.

        Args:
            self: (todo): write your description
        """
        super(TestContextLocalData, self).setUp()

        self.test_context_local_data = _ContextLocalData("test", None)

    @property
    @abstractmethod
    def proxy_object(self):
        """
        Get the proxy object.

        Args:
            self: (todo): write your description
        """
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
        """
        Return a proxy object.

        Args:
            self: (todo): write your description
        """
        return g

    def test_set(self):
        """
        Sets the test test test test_set.

        Args:
            self: (todo): write your description
        """
        self._test_set()

    def test_set_outside_context(self):
        """
        Sets the test context.

        Args:
            self: (todo): write your description
        """
        self._test_set_outside_context()

    def test_get(self):
        """
        Get test test test test.

        Args:
            self: (todo): write your description
        """
        self._test_get()

    def test_get_outside_context(self):
        """
        Gets the test context.

        Args:
            self: (todo): write your description
        """
        self._test_get_outside_context()

    def test_get_default_value(self):
        """
        Returns the test value

        Args:
            self: (todo): write your description
        """
        self._test_get_default_value()
