from dataclasses import dataclass
from enum import Enum
from typing import Union, Callable, Type

from flask import Flask
from pydantic import ValidationError, NoneIsNotAllowedError, BoolError, BaseModel
from pydantic.error_wrappers import ErrorWrapper
from werkzeug.exceptions import HTTPException, PreconditionFailed
from werkzeug.routing import RequestRedirect

from app.hooks.error import broad_exception_handler
from tests import BaseTestCase


@dataclass
class ExceptionHandlingSpec:
    error_handler_exception_or_code: Union[Type[Exception], int]
    error_handler_func: Callable
    exception_instance_to_handler_raises: Exception


class TestError(BaseTestCase):
    def setUp(self):
        super(TestError, self).setUp()

        self.path = "/foo"

    def add_route_raises_exception(
        self, exception_handling_spec: ExceptionHandlingSpec
    ):
        self.app = Flask(__name__)
        self.app.register_error_handler(
            exception_handling_spec.error_handler_exception_or_code,
            exception_handling_spec.error_handler_func,
        )
        self.client = self.app.test_client()

        @self.app.route(self.path)
        def handler():
            raise exception_handling_spec.exception_instance_to_handler_raises


class TestBroadExceptionHandler(TestError):
    def test_http_exception(self):
        for exception_cls in HTTPException.__subclasses__():
            if exception_cls in (RequestRedirect, PreconditionFailed):
                continue

            exception_instance = exception_cls()

            self.add_route_raises_exception(
                ExceptionHandlingSpec(
                    Exception, broad_exception_handler, exception_instance
                )
            )

            resp = self.request()

            self.assertEqual(exception_instance.code, resp.status_code)
            self.assertTrue(resp.is_json)
            self.assertDictEqual({"error": exception_instance.description}, resp.json)

    def test_pydantic_validation_error(self):
        self.add_route_raises_exception(
            ExceptionHandlingSpec(
                Exception,
                broad_exception_handler,
                ValidationError(
                    [
                        ErrorWrapper(NoneIsNotAllowedError(), "foo"),
                        ErrorWrapper(BoolError(), "bar"),
                    ],
                    BaseModel,
                ),
            )
        )

        resp = self.request()

        self.assertEqual(400, resp.status_code)
        self.assertDictEqual(
            {
                "error": [
                    {
                        "loc": ["foo"],
                        "msg": "none is not an allowed value",
                        "type": "type_error.none.not_allowed",
                    },
                    {
                        "loc": ["bar"],
                        "msg": "value could not be parsed to a boolean",
                        "type": "type_error.bool",
                    },
                ]
            },
            resp.json,
        )

    def test_pydantic_validation_error_with_enum(self):
        class Example(BaseModel):
            class Choices(Enum):
                A = 1
                B = 2
                C = 3

            c: Choices

        try:
            Example(c=4)
        except ValidationError as e:
            self.add_route_raises_exception(
                ExceptionHandlingSpec(Exception, broad_exception_handler, e,)
            )

        resp = self.request()

        self.assertEqual(400, resp.status_code)
        self.assertDictEqual(
            {
                "error": [
                    {
                        "ctx": {"enum_values": [1, 2, 3]},
                        "loc": ["c"],
                        "msg": "value is not a valid enumeration member; permitted: 1, 2, 3",
                        "type": "type_error.enum",
                    }
                ]
            },
            resp.json,
        )

    def test_500(self):
        self.add_route_raises_exception(
            ExceptionHandlingSpec(Exception, broad_exception_handler, KeyError())
        )

        resp = self.request()

        self.assertEqual(500, resp.status_code)
        self.assertDictEqual({"error": ""}, resp.json)
