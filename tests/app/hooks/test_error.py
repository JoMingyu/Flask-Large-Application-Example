from werkzeug.exceptions import HTTPException
from werkzeug.routing import RequestRedirect

from tests import BaseTestCase


class TestError(BaseTestCase):
    def setUp(self):
        super(TestError, self).setUp()

        self.path = '/foo'

    def add_route_raises_exception(self, exception_cls):
        self.app.view_functions.pop('handler', None)

        @self.app.route(self.path)
        def handler():
            raise exception_cls()


class TestHTTPExceptionHandler(TestError):
    def test(self):
        for exception_cls in HTTPException.__subclasses__():
            if exception_cls is RequestRedirect or exception_cls.code == 412:
                continue

            self.add_route_raises_exception(exception_cls)

            resp = self.request()
            self.assertEqual(exception_cls.code, resp.status_code)
            self.assertTrue(resp.is_json)
            self.assertDictEqual({
                'message': exception_cls.description
            }, resp.json)


class TestBroadExceptionHandler(TestError):
    # TODO broad_exception_handler가 세분화될 때마다 테스트 케이스 추가

    def test_500(self):
        self.add_route_raises_exception(Exception)

        resp = self.request()
        self.assertEqual(500, resp.status_code)
        self.assertEqual('', resp.data.decode())
